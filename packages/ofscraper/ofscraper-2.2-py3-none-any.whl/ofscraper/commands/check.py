import logging
import re
import asyncio
import textwrap
import httpx
import arrow
from textual.app import App, ComposeResult
from textual.widgets import Input,ContentSwitcher,DataTable, Button,Switch,Label,Select,Checkbox
from rich.text import Text
from textual.containers import Horizontal, VerticalScroll,Vertical
from textual import events
import ofscraper.utils.args as args_
import ofscraper.db.operations as operations
import ofscraper.api.profile as profile
import ofscraper.utils.auth as auth
import ofscraper.api.timeline as timeline
import ofscraper.api.messages as messages_
import ofscraper.api.posts as posts_
import ofscraper.constants as constants
import ofscraper.api.paid as paid_

from diskcache import Cache
from ..utils.paths import getcachepath
cache = Cache(getcachepath())

log = logging.getLogger(__package__)
args = args_.getargs()
ROW_NAMES="Number","UserName","Downloaded","Unlocked","Double_Purchase","Length","Mediatype", "Post_Date","Post_Media_Count","Responsetype", "Price", "Post_ID","Media_ID","Text"




def post_checker():
    headers = auth.make_headers(auth.read_auth())
    user_dict = {}
    client = httpx.Client(http2=True, headers=headers)
    links=url_helper()
    for ele in list(filter(lambda x: re.search("onlyfans.com/[a-z_]+$", x), links)):
        name_match = re.search("/([a-z_]+$)", ele)
        if name_match:
            user_name=name_match.group(1)
            log.info(f"Getting Full Timeline for {user_name}")

            model_id=profile.get_id(headers,user_name)
            oldtimeline=cache.get(f"timeline_check_{model_id}",default=[])
            if len(oldtimeline)>0 and not args.force:
                user_dict[user_name]=oldtimeline
            elif not user_dict.get(user_name):
                user_dict[user_name] = {}
                user_dict[user_name] = user_dict[user_name] or []
                user_dict[user_name].extend(asyncio.run(timeline.get_timeline_post(headers,model_id)))
                user_dict[user_name].extend(timeline.get_pinned_post(headers,model_id))
                user_dict[user_name].extend(timeline.get_archive_post(headers,model_id))
                cache.set(f"timeline_check_{model_id}",user_dict[user_name],expire=constants.CHECK_EXPIRY)

    #individual links
    for ele in list(filter(lambda x: re.search("onlyfans.com/[0-9]+/[a-z_]+$", x), links)):
        name_match = re.search("/([a-z]+$)", ele)
        num_match = re.search("/([0-9]+)", ele)
        if name_match and num_match:
            model_id=num_match.group(1)
            user_name=name_match.group(1)
            log.info(f"Getting Invidiual Link for {user_name}")

            if not user_dict.get(user_name):
                user_dict[name_match.group(1)] = {}
            data = timeline.get_individual_post(model_id, client)
            user_dict[user_name] = user_dict[user_name] or []
            user_dict[user_name].append(data)
    app_run_helper(user_dict)





     
def message_checker():
    links=url_helper()
    ROWS = get_first_row()
    user_dict={}
    for item in links:
        num_match = re.search("/([0-9]+)", item)
        headers = auth.make_headers(auth.read_auth())
        if num_match:
            model_id = num_match.group(1)
            user_name = profile.scrape_profile(headers, model_id)['username']
            user_dict[user_name]=user_dict.get(user_name,[])
            log.info(f"Getting Messages for {user_name}")
            messages=None
            oldmessages=cache.get(f"message_check_{model_id}",default=[])

            #start loop
            if len(oldmessages)>0 and not args.force:
                messages=oldmessages
            else:
                messages=asyncio.run(messages_.get_messages(headers,  model_id))
                cache.set(f"message_check_{model_id}",messages,expire=constants.CHECK_EXPIRY)
            user_dict[user_name].extend(messages)
        
    app_run_helper(user_dict)

def purchase_checker():
    user_dict={}
    headers = auth.make_headers(auth.read_auth())
    for user_name in args.username:
        user_dict[user_name]=user_dict.get(user_name, [])
        model_id = profile.get_id(headers, user_name)
        oldpaid=cache.get(f"purchased_check_{model_id}",default=[])
        paid=None
        #start loop
        if len(oldpaid)>0 and not args.force:
            paid=oldpaid
        else:
            paid=paid_.scrape_paid(user_name)
            cache.set(f"purchased_check_{model_id}",paid,expire=constants.CHECK_EXPIRY)
        user_dict[user_name].extend(paid)
    app_run_helper(user_dict)
 


def url_helper():
    out=[]
    out.extend(args.file or [])
    out.extend(args.url or [])
    return map(lambda x:x.strip(),out)
    
    
def app_run_helper(user_dict):
    headers = auth.make_headers(auth.read_auth())
    ROWS = get_first_row()
    for user_name in user_dict.keys():
        temp = []
        model_id = profile.get_id(headers, user_name)
        operations.create_tables(model_id,user_name)
        downloaded={}
        [downloaded.update({ele:downloaded.get(ele,0)+1}) for ele in operations.get_media_ids(model_id, user_name)]
        [temp.extend(ele.all_media) for ele in map(lambda x:posts_.Post(
            x, model_id, user_name), user_dict[user_name])]

        ROWS.extend(add_rows(temp,downloaded,user_name))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = InputApp()
    # we have to set properies before run
    app.table_data = ROWS
    app.row_names=ROW_NAMES
    app.set_filtered_rows(reset=True)
    app.run()



def get_first_row():
    return [ROW_NAMES]
def texthelper(text):
    text=textwrap.dedent(text)
    text=re.sub(" +$","",text)
    text=re.sub("^ +","",text)
    text = re.sub("<[^>]*>", "", text) 
    text=text if len(text)<constants.TABLE_STR_MAX else f"{text[:constants.TABLE_STR_MAX]}..."
    return text
def unlocked_helper(ele,mediaset):
    return ele.canview
def datehelper(date):
    if date=="None":
        return "Probably Deleted"
    return arrow.get(date).format("YYYY-MM-DD hh:mm A")
def duplicated_helper(ele,mediadict,downloaded):
    if ele.value=="free":
        return False
    elif len(list(filter(lambda x:x.canview,mediadict.get(ele.id,[]))))>1:
        return True
    elif downloaded.get(ele,0)>2:
        return True
    else:
        return False
def add_rows(media,downloaded,username):
    #fix text
    mediaset=set(map(lambda x:x.id,filter(lambda x:x.canview,media)))
    mediadict={}
    [mediadict.update({ele.id:mediadict.get(ele.id,[])+ [ele]}) for ele in media]

    for ele in media:   
        return map(lambda x: (x[0],username,x[1].id in downloaded,unlocked_helper(x[1],mediaset),duplicated_helper(x[1],mediadict,downloaded),x[1].length_,x[1].mediatype,datehelper(x[1].postdate),len(ele._post.post_media),x[1].responsetype ,"Free" if x[1]._post.price==0 else "{:.2f}".format(x[1]._post.price),  x[1].postid,x[1].id,texthelper(x[1].text)), enumerate(media))



class StyledButton(Button):
    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

class StringField(Horizontal):
        def __init__(self, name: str) -> None:
            super().__init__(id=name)
            self.filter_name = name
        def compose(self):
            yield Input(placeholder=self.filter_name.capitalize(),id=f"{self.filter_name}_search")
        def on_mount(self):
            self.styles.padding=1
            self.styles.height="15vh"
            self.styles.width="100%"
        def update_table_val(self,val):
            self.query_one(Input).value=val
        def reset(self):
            self.query_one(Input).value=""
        def validate(self,val):
             if self.query_one(Input).value=="" or self.query_one(Input).value==None:
                 return True
             elif re.fullmatch(self.query_one(Input).value,str(val),re.IGNORECASE):
                    return True
             return False
             
        
                
            

class NumField(Horizontal):
        def __init__(self, name: str) -> None:
            super().__init__(id=name)
            self.filter_name = name
        def compose(self):
            yield self.IntegerInput(placeholder=self.filter_name.capitalize(),id=f"{self.filter_name}_search")
        def on_mount(self):
            self.styles.padding=1
            self.styles.height="15vh"
            self.styles.width="100%"
        def update_table_val(self,val):
            self.query_one(self.IntegerInput).value=val
        def reset(self):
            self.query_one(self.IntegerInput).value=""
        def validate(self,val):
             if self.query_one(self.IntegerInput).value=="":
                 return True
             if int(val)==int(self.query_one(self.IntegerInput).value):
                 return True
             return False            
        class IntegerInput(Input):
            def __init__(
                self,
                *args,**kwargs
                # ---snip---
            ) -> None:
                super().__init__(
                    # ---snip---
                    *args,**kwargs
                )

            def insert_text_at_cursor(self, text: str) -> None:
                try:
                    int(text)
                except ValueError:
                    pass
                else:
                    super().insert_text_at_cursor(text)


        
            
                 

class PriceField(Horizontal):
        def __init__(self, name: str) -> None:
            super().__init__(id=name)
            self.filter_name = name
        def compose(self):
            yield self.IntegerInput(placeholder=self.filter_name.capitalize(),id=f"{self.filter_name}_search")
        def on_mount(self):
            self.styles.padding=1
            self.styles.height="15vh"
            self.styles.width="100%"
        def update_table_val(self,val):
            self.query_one(self.IntegerInput).value=val            
        def reset(self):
            self.query_one(self.IntegerInput).value=""
        def validate(self,val):
             if self.query_one(self.IntegerInput).value=="":
                 return True
             if float(val)==float(self.query_one(self.IntegerInput).value):
                 return True
             return False            
        class IntegerInput(Input):
            def __init__(
                self,
                *args,**kwargs
                # ---snip---
            ) -> None:
                super().__init__(
                    # ---snip---
                    *args,**kwargs
                )

            def insert_text_at_cursor(self, text: str) -> None:
                try:
                    if text!=".":
                        int(text)
                except ValueError:
                    pass
                else:
                    super().insert_text_at_cursor(text)                          
class TimeField(Horizontal):
        def __init__(self, name: str) -> None:
            super().__init__(id=name)
            self.filter_name = name
        def compose(self):
            yield self.IntegerInput(placeholder="Longer",id=f"{self.filter_name}_search")
            yield self.IntegerInput(placeholder="Shorter",id=f"{self.filter_name}_search2")

        def on_mount(self):
            self.styles.padding=1
            self.styles.height="15vh"
            self.styles.width="100%"
        def update_table_val(self,val):
            for ele in self.query(self.IntegerInput):
                ele.value=self.convertString(val)
        def reset(self):
            for ele in self.query(self.IntegerInput):
                ele.value=""
        def convertString(self,val):
            if val=="N/A":
                return 0
            if isinstance(val,int):
                return val
            elif val.find(":")!=-1:
                 a=val.split(":")
                 return (int(a[0])*60*60)+(int(a[1])*60)+(int(a[2])*1)
            return int(val)
        def validate(self,val):
             [setattr(ele,"value",self.convertString(ele.value)) for ele in self.query(self.IntegerInput)]
             val=self.convertString(val)
             if len(list(filter(lambda x:x.value=="",self.query(self.IntegerInput))))==2:
                 return True
             if val<self.query_one(f"#{self.filter_name}_search").value:
                 return False
             if val>self.query_one(f"#{self.filter_name}_search2").value:
                 return False
             return True            
        class IntegerInput(Input):
            def __init__(
                self,
                *args,**kwargs
                # ---snip---
            ) -> None:
                super().__init__(
                    # ---snip---
                    *args,**kwargs
                )

            def insert_text_at_cursor(self, text: str) -> None:
                try:
                    if text!=":":
                        int(text)
                except ValueError:
                    pass
                else:
                    super().insert_text_at_cursor(text)                          

class BoolField(Horizontal):
        def __init__(self, name: str) -> None:
            super().__init__(id=name,classes="container")
            self.filter_name = name
        def on_mount(self):
            [setattr(ele,"styles.width","30%") for ele in self.query(Checkbox)]
        def compose(self):
            yield Checkbox(f"{self.filter_name.capitalize()} True",True,id=f"{self.filter_name}_search")
            yield Checkbox(f"{self.filter_name.capitalize()} False",True,id=f"{self.filter_name}_search2")
            self.styles.height="15vh"
            self.styles.width="100%"
        def update_table_val(self,val):
            if val=="True":
                self.query_one(f"#{self.filter_name}_search").value=True 
                self.query_one(f"#{self.filter_name}_search2").value=False
            elif val=="False" :
                self.query_one(f"#{self.filter_name}_search2").value=True
                self.query_one(f"#{self.filter_name}_search").value=False
 
     
        def reset(self):
            for ele in self.query(self.IntegerInput):
                ele.value=True
        def validate(self,val):
             
             if val==True and not self.query_one(f"#{self.filter_name}_search").value:
                 return False
             elif val==False and not self.query_one(f"#{self.filter_name}_search2").value:
                 return False
             
             return True
class MediaField(Horizontal):
        def __init__(self, name: str) -> None:
            super().__init__(id=name,classes="container")
            self.filter_name = name
        def on_mount(self):
            [setattr(ele,"styles.width","30%") for ele in self.query(Checkbox) ]
        def compose(self):
            yield Checkbox("audios",True,id=f"{self.filter_name}_search")
            yield Checkbox("videos",True,id=f"{self.filter_name}_search2")
            yield Checkbox("Images",True,id=f"{self.filter_name}_search3")
            self.styles.height="15vh"
            self.styles.width="100%"
        def update_table_val(self,val):
            if val=="audios":
                self.query_one(f"#{self.filter_name}_search").value=True
                self.query_one(f"#{self.filter_name}_search2").value=False
                self.query_one(f"#{self.filter_name}_search3").value=False
            elif val=="videos":
                self.query_one(f"#{self.filter_name}_search2").value=True
                self.query_one(f"#{self.filter_name}_search3").value=False
                self.query_one(f"#{self.filter_name}_search").value=False
            elif val=="images":
                self.query_one(f"#{self.filter_name}_search3").value=True
                self.query_one(f"#{self.filter_name}_search").value=False
                self.query_one(f"#{self.filter_name}_search2").value=False



        def reset(self):
            for ele in self.query(Checkbox):
                ele.value=True
        def validate(self,val):
            if val=="audios" and not self.query_one(f"#{self.filter_name}_search").value:
                return False
            elif val=="videos" and not self.query_one(f"#{self.filter_name}_search2").value:
                return False
            elif val=="images" and not self.query_one(f"#{self.filter_name}_search3").value:
                return False
            return True

                         
class DateField(Horizontal):
        def __init__(self, name: str) -> None:
            super().__init__(id=name,classes="container")
            self.filter_name = name
        def compose(self):
            yield Input(placeholder="After",id=f"{self.filter_name}_search")
            yield Input(placeholder="Before",id=f"{self.filter_name}_search2")


        def on_mount(self):
            self.styles.padding=1
            self.styles.height="15vh"
            self.styles.width="100%"
            for ele in self.query(Input):
                ele.styles.width="1fr"
        def update_table_val(self,val): 
            val=self.convertString(val)
            for ele in self.query(Input): 
                if val!="":
                    ele.value=arrow.get(val).format("YYYY.MM.DD")   
                else:
                    ele.value=""     
        def reset(self):
            for ele in self.query(Input):
                ele.styles.width=""
        def validate(self,val):
            val=self.convertString(val)
            if len(list(filter(lambda x:x.value=="",self.query(Input))))==2:
                return True
            try:
                if arrow.get(val)<arrow.get(self.query_one(f"#{self.filter_name}_search").value):
                    return False
                if arrow.get(val)>arrow.get(self.query_one(f"#{self.filter_name}_search2").value):
                    return False
                return True
            except:
                return True
        def convertString(self,val):
            match=re.search("[0-9-/]+",val)
            if not match:
                return ""
            return match.group(0)



                         

class InputApp(App):

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.exit()
        if event.key=="end":
            table = self.query_one(DataTable)
            cursor_coordinate = table.cursor_coordinate
            if len(table._data) == 0:
                return
            cell_key = table.coordinate_to_cell_key(cursor_coordinate)
            event=DataTable.CellSelected(
                self,
                table.get_cell_at(cursor_coordinate),
                coordinate=cursor_coordinate,
                cell_key=cell_key,
                )
            row_name=self.row_names[event.coordinate[1]]
            self.update_input(row_name,event.value.plain)        
            self.set_filtered_rows()
            self.make_table()

            

    def compose(self) -> ComposeResult:
        with Horizontal(id="buttons"):
            yield StyledButton("Table", id="data-table")
            yield StyledButton("Filters", id="settings")
            
        yield StyledButton("Reset", id="reset")
       
        with ContentSwitcher(initial="data-table_page"):  
            with Vertical(id="settings_page"):
                yield StyledButton("Submit", id="submit")
                with VerticalScroll():
                    for ele in ["Text"]:
                        yield StringField(ele)
                    for ele in ["Media_ID","Post_ID","Post_Media_Count"]:
                        yield NumField(ele)
                    for ele in ["Length"]:
                        yield TimeField(ele)    
                    for ele in ["Price"]:
                        yield PriceField(ele)
                    for ele in ["Downloaded","Unlocked","Double_Purchase"]:
                        yield BoolField(ele)
                    for ele in ["Post_Date"]:
                        yield DateField(ele)
                    for ele in ["Mediatype"]:
                        yield MediaField(ele)
            yield DataTable(fixed_rows=1,id="data-table_page")


            
                
            
 
        

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id=="submit":
            self.set_filtered_rows()
            self.make_table()
        elif event.button.id=="reset":
            self.set_filtered_rows(reset=True)
            self.reset_all_inputs()
            self.make_table()

            
        else:
            self.query_one(ContentSwitcher).current = f"{event.button.id}_page"
    

    def on_mount(self) -> None:
        self.make_table()
        self.query_one("#buttons").styles.padding=1
        self.query_one("#buttons").styles.height="20%"
        self.query_one("#buttons").styles.align = ("center", "middle")
        self.query_one("#reset").styles.align = ("center", "middle")


        self.query_one("#submit").styles.dock="top"
        self.query_one("#settings_page").query_one(VerticalScroll).padding=1
        self.query_one(DataTable).styles.min_height="30vh"
        self.query_one(DataTable).styles.max_height="60vh"





    def set_filtered_rows(self,reset=False):
        if reset==True:
            self._filtered_rows=self.table_data[1:]
        else:     
            self._filtered_rows=filter(lambda x:self.row_allowed(x)==True,self.table_data[1:])


    def row_allowed(self,row):
        for count,name in enumerate(self.row_names[1:]):
            try:
                targetNode=self.query_one(f"#{name}")
                if targetNode.validate(row[count+1]):
                    continue
                return False
            except:
                None
        return True


    def update_input(self,row_name,value):
        try:
            targetNode=self.query_one(f"#{row_name}")
            targetNode.update_table_val(value)
        except:
            None
    
    def reset_all_inputs(self):
        for ele in self.row_names[1:]:
            try:
                self.query_one(f"#{ele}").reset()
            except:
                continue
           


      
          

          





    def make_table(self):
        table = self.query_one(DataTable)
        table.clear(True)
        table.fixed_rows = 0
        table.zebra_stripes=True
        [table.add_column(re.sub("_"," ",ele),key=str(ele)) for ele in self.table_data[0]]
        for count, row in enumerate(self._filtered_rows):
            # Adding styled and justified `Text` objects instead of plain strings.
            styled_row = [
                Text(str(cell), style="italic #03AC13") for cell in row
            ]
            table.add_row(*styled_row, key=str(count+1))

        if len(table.rows)==0:
            table.add_row("All Items Filtered")

