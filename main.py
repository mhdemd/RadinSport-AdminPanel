from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivymd.uix.behaviors import CommonElevationBehavior
from libs.py_files.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.loader import Loader
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast

import requests
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from functools import partial
import urllib.request

#from kivy.config import Config
#Config.set('graphics', 'width', '800')
#Config.set('graphics', 'height', '600')
#Config.set('graphics', 'fullscreen', 'auto')

import os
import sys
from pathlib import Path
from PIL import Image

if getattr(sys, "frozen", False):  # bundle mode with PyInstaller
    os.environ["RADIN_ROOT"] = sys._MEIPASS
else:
    os.environ["RADIN_ROOT"] = str(Path(__file__).parent)

Window.size = 1280, 720


Builder.load_file('main.kv')
Builder.load_file(f"{os.environ['RADIN_ROOT']}/libs/kv files/order.kv")
Builder.load_file(f"{os.environ['RADIN_ROOT']}/libs/kv files/products.kv")

class MobileView(MDScreen):
    pass

class TabletView(MDScreen):
    pass

class DesktopView(MDScreen):
    pass

class Product_table(MDScreen):
    pass

class Order_first_section(MDBoxLayout):
    order_number = ObjectProperty()
    order_status = ObjectProperty()
    see_order_det = ObjectProperty()

class RV_orders(RecycleView):

    def __init__(self, **kwargs):
        super(RV_orders, self).__init__(**kwargs)
        self.data = []#[item for item in items_in_orders]  

class Order_detail_top_box(MDBoxLayout):
    order_num = ObjectProperty()
    receiver = ObjectProperty()
    tel = ObjectProperty()
    address = ObjectProperty()
    total = ObjectProperty()
    status = ObjectProperty()

class Order_detail_bottom_box(MDBoxLayout):
    title = ObjectProperty()
    image = ObjectProperty()
    total = ObjectProperty()
    color_en = ObjectProperty()
    color_fa = ObjectProperty()
    num_order = ObjectProperty()
    num_order = ObjectProperty()

class ImageButton(ButtonBehavior, AsyncImage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Product_first_MDSmartTile(MDSmartTile, CommonElevationBehavior):
    pass

class Product_detail_image(MDBoxLayout, Button):
    source = ObjectProperty()
    icon_color = ObjectProperty()

class Content(BoxLayout):
    pass#error = ObjectProperty()

class Product_detail_BoxLayout(BoxLayout):
    title= ObjectProperty()
    code= ObjectProperty()
    category= ObjectProperty()
    dkp= ObjectProperty()
    material= ObjectProperty()
    country= ObjectProperty()
    type= ObjectProperty()
    dt1= ObjectProperty()
    dt2= ObjectProperty()
    dt3= ObjectProperty()
    dt4= ObjectProperty()

class ResponsiveView(MDResponsiveLayout, MDScreen):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mobile_view = MobileView()
        self.tablet_view = TabletView()
        self.desktop_view = DesktopView()
        self.category_dict = {"Hats and Masks" : "H",
                    "Sport Gloves" : "GL",
                    "Swimming Accessories" : "SW",
                    "Pilates and Fitness" : "PI",
                    "Bottles and Shakers" : "SH",
                    "Jump Ropes" : "R",                       
                    }

    def update_order_status(self, text_item, order_number):
        
        # API To change the order status
        # Get data from APIs 
        url = 'http://mahdiemadi.ir/support_update_status' 

        # Define the request parameters
        data = {'variable1': order_number, 'variable2': text_item}

        try:
            response = requests.post(url, data=data, timeout=2)            
        except:
            print('No conn')
            return

        results = response
        
        self.desktop_view.ids._orders.ids._Order_detail.ids._Order_detail_sc.children[0].status = text_item
        self.menu.dismiss()
        
        next((item.update({'order_status': get_display(reshape('وضعیت:      %s'%(text_item)))   }) for item in self.items_in_orders if item['order_number'].startswith('%s'%(order_number))), None)

        self.desktop_view.ids._orders.ids._Order_first.ids._RV_orders.refresh_from_data()

    def see_orders(self, *arg):

        self.items_in_orders = []

        # To avoid reloading 
        self.grouping = False

        # Get data from APIs 
        url = 'http://mahdiemadi.ir/see_orders' 

        # Define the request parameters
        params = {'variable': '1000'}

        try:
            response3 = requests.get(url, params=params, timeout=2)            
        except:
            print('No conn')
            return

        results = response3.json()

        if results == []:
            try:
                if self.pop_up:
                    self.pop_up.dismiss()
            except: 
                pass
            content = Button(text= get_display(reshape('بازگشت')), font_name= 'font/IRANSansXFaNum-Medium.ttf', size_hint=(1, None), size=('20mm', '6mm'))
            pop = Popup(title= get_display(reshape('سفارشی ثبت نشده است!')), title_font = 'font/IRANSansXFaNum-Medium.ttf', content= content,
            title_align= 'center', size_hint=(None, None), size=(self.width , '20mm'),separator_height= 0)
            content.bind(on_release=pop.dismiss)
            pop.open()
            return

        # Create list of order number & order status
        list_orders = []
        list_status = []

        seen_first_items = set()

        # Iterate over the order_list
        for sublist in results:
            first_item = sublist[0]
            third_item = sublist[2]
            
            if first_item not in seen_first_items:
                seen_first_items.add(first_item)
                list_orders.append(first_item)
                list_status.append(third_item)

        # Forming a list of order_numbers
        for i in range(len(list_orders)):

            self.items_in_orders.append(
                {
                    'order_number': get_display(reshape('شماره سفارش: %s'%(list_orders[i]))),
                    'see_order_det': get_display(reshape('جزییات سفارش')),
                    'order_status': get_display(reshape('وضعیت:      %s'%(list_status[i]))),
                }
            )
        sorted_data = sorted(self.items_in_orders, key=lambda x: int(x['order_number'].split(':')[0]), reverse=True)
        self.desktop_view.ids._orders.ids._Order_first.ids._RV_orders.data = sorted_data
        self.desktop_view.ids._orders.ids._Order_first.ids._RV_orders.refresh_from_data()
        snackbar = Snackbar(text="Orders are updated", size_hint= (.25, None), height= '8mm' , pos_hint= {'right': 1})
        snackbar.open()

    def see_order_detail(self, *arg):

        self.desktop_view.ids._orders.ids._Order_detail.ids._Order_detail_sc.clear_widgets()
        order_number = arg[0].split(':')[0].strip()

        # Get data from APIs 
        url = 'http://mahdiemadi.ir/see_order_detail' 

        # Define the request parameters
        params = {'variable1': order_number, 'variable2': '1000'}

        try:
            response3 = requests.get(url, params=params, timeout=2)            
        except:
            print('No conn')

        results = response3.json()
        
        address1 = results['customer'][0][3].split(', ')[1:3]
        address2 = results['customer'][0][3].split(', ')[3:4] 
        
        tot = 0
        for item in results['order']:
            tot += item[2] * item[6]

        order_detail_top_box = Order_detail_top_box(
            order_num='%s'%(order_number), 
            receiver= '%s %s'%(get_display(reshape(results['customer'][0][0])), get_display(reshape(results['customer'][0][1]))),
            tel= int(results['customer'][0][2]), 
            address= get_display(reshape('%s, %s\n\n%s\n\n%s'
                        %(address1[1], address1[0], address2[0], results['customer'][0][4]))),
            total= f'{tot:,}', 
        )
        for i in range(len(results['order'])):
            price = results['order'][i][6]      
            det_order_box_box = Order_detail_bottom_box(
                title= results['order'][i][5], 
                image= results['order'][i][4],
                total= f'{price:,}',
                num_order= results['order'][i][2], 
                color_en= results['order'][i][7], 
                color_fa= results['order'][i][8], 
            )

            order_detail_top_box.add_widget(det_order_box_box)
            order_detail_top_box.add_widget(Factory.Widget1())


        self.desktop_view.ids._orders.ids._Order_detail.ids._Order_detail_sc.add_widget(order_detail_top_box)

        # Add status drop down menu
        menu_items = [
            {
                "viewclass": "Label",
                'size_hint_y': None,
                'height': 3
            },
            {
                "text": get_display(reshape('سفارش جدید')),
                'font_name': 'font/IRANSansXFaNum-Medium.ttf',
                'halign': 'center',
                "viewclass": "MDRaisedButton",
                'size_hint_x': .8, 
                'pos_hint': {'center_x': .5},
                "on_release": lambda x=f"{'سفارش جدید'}": self.update_order_status(x, order_number),
                'md_bg_color': Test.get_running_app().theme_cls.primary_dark
            },
            {
                "viewclass": "Label",
                'size_hint_y': None,
                'height': 3,
            },
            {
                "text": get_display(reshape('در حال پردازش')),
                'font_name': 'font/IRANSansXFaNum-Medium.ttf',
                'halign': 'center',
                "viewclass": "MDRaisedButton",
                'size_hint_x': .8,
                'pos_hint': {'center_x': .5},
                "on_release": lambda x=f"{'در حال پردازش'}": self.update_order_status(x, order_number),
                'md_bg_color': Test.get_running_app().theme_cls.primary_dark
            },
            {
                "viewclass": "Label",
                'size_hint_y': None,
                'height': 3
            },
            {
                "text": get_display(reshape('در حال ارسال')),
                'font_name': 'font/IRANSansXFaNum-Medium.ttf',
                'halign': 'center',
                "viewclass": "MDRaisedButton",
                'size_hint_x': .8,
                'pos_hint': {'center_x': .5},
                "on_release": lambda x=f"{'در حال ارسال'}": self.update_order_status(x, order_number),
                'md_bg_color': Test.get_running_app().theme_cls.primary_dark
            },
            {
                "viewclass": "Label",
                'size_hint_y': None,
                'height': 3
            },
            {
                "text": get_display(reshape('تحویل شده')),
                'font_name': 'font/IRANSansXFaNum-Medium.ttf',
                'halign': 'center',
                "viewclass": "MDRaisedButton",
                'size_hint_x': .8,
                'pos_hint': {'center_x': .5},
                "on_release": lambda x=f"{'تحویل شده'}": self.update_order_status(x, order_number),
                'md_bg_color': Test.get_running_app().theme_cls.primary_dark
            },
            {
                "viewclass": "Label",
                'size_hint_y': None,
                'height': 3
            },
            {
                "text": get_display(reshape('کنسل شده')),
                'font_name': 'font/IRANSansXFaNum-Medium.ttf',
                'halign': 'center',
                "viewclass": "MDRaisedButton",
                'size_hint_x': .8,
                'pos_hint': {'center_x': .5},
                "on_release": lambda x=f"{'کنسل شده'}": self.update_order_status(x, order_number),
                'md_bg_color': Test.get_running_app().theme_cls.primary_dark
            },

        ]

        self.menu = MDDropdownMenu(
            caller= self.desktop_view.ids._orders.ids._Order_detail.ids._Order_detail_sc.children[0].mgr1,
            items=menu_items,
            width_mult= '.7mm',
            max_height= '58mm',
            radius=[24, 0, 24, 0],
            elevation=4
        )

        self.desktop_view.ids._orders.ids._Order_detail.ids._Order_detail_sc.children[0].status = results['order'][-1][-1]

    def search_action(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Search:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=Test.get_running_app().theme_cls.primary_color,
                        on_press=self.search_action_close
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=Test.get_running_app().theme_cls.primary_color,
                        on_press=partial(self.search_by_code)
                    ),
                ],
            )
        self.dialog.open()

    def search_by_code(self, *args):
        code = self.dialog.content_cls.ids._code.text

        # API To change the order status
        # Get data from APIs
        url = 'http://mahdiemadi.ir/search_dkp'

        # Define the request parameters
        params = {'variable1': code}

        try:
            response = requests.get(url, params=params, timeout=2)
        except:
            print('No conn')
            return

        results = response.json()

        if results == []:
            self.dialog.content_cls.ids._code.error = True
            self.dialog.content_cls.ids._code.helper_text = "No result found"
            return

        results = response.json()

        results = sorted(results, key=lambda x: x[2])
        result_tuples = []
        max_counter = 0

        for row in results:
            counter = max_counter + 1
            max_counter = counter
            
            counter_str = str(counter)
            image_path = 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(row[0], row[0])
            color = [1, 0, 0, 1]
            font_text = '[font=font/IRANSansXFaNum-Medium.ttf]%s[/font]' % row[1]
            date_text = (row[2].split('-'))[0] + '-' + (row[2].split('-'))[1]
            other_data = tuple(row[3:-1])
            
            item = (
                counter_str + "-       [color=#FFFFFF].[/color]",
                (image_path, color, font_text),
                date_text,
            ) + other_data
            
            result_tuples.append(item)

        result_tuples = sorted(result_tuples, key=lambda x: int(x[0].split('-')[0]))

        self.data_tables = MDDataTable(
            effect_cls= 'ScrollEffect',
            use_pagination=True,
            rows_num= 10,
            elevation=2,
            size_hint_y= 1,
            pos_hint= {'center_x': .5},
            column_data=
            [   ("No.", dp(.1)),
                ("Title", dp(45) ),#, self.sort_on_signal),
                ("           Code", dp(5) ),
                ("      [size=15]Avg. stock[/size]", dp(9) ),
                ("      Min. price", dp(12) ),
                ("      [size=15]Disc.(%)[/size]", dp(9) ),#, self.sort_on_schedule),
                ("           [size=15]Disc. price[/size]", dp(12) ),#, self.sort_on_team),
            ],

            row_data= result_tuples, 
        )
        #self.data_tables.bind(on_row_press=self.on_row_press)
        #self.data_tables.bind(on_check_press=self.on_check_press)

        if self.desktop_view.ids._Product.has_screen('search'):
            #print('has_screen')
            box_layout = self.search_screen.ids._Product_table_MDBoxLayout
            first_child = box_layout.children[0]
            box_layout.remove_widget(first_child)

            self.search_screen.ids._Product_table_MDBoxLayout.add_widget(self.data_tables)
            self.search_screen.ids._Product_table_MDTopAppBar.title = 'Search result'

        else:
            #print('has_nooooooooooot_screen')
            self.search_screen = Product_table(name= 'search')

            self.search_screen.ids._Product_table_MDBoxLayout.add_widget(self.data_tables)
            self.search_screen.ids._Product_table_MDTopAppBar.title = 'Search result'
            self.desktop_view.ids._Product.add_widget(self.search_screen)

        self.desktop_view.ids._Product.current = 'search' 
        
        self.search_action_close()

    def search_action_close(self, *args):
        self.dialog.dismiss()

    def open_category_table(self, category):
        
        if self.desktop_view.ids._Product.has_screen(self.category_dict[category]):
            self.desktop_view.ids._Product.current = self.category_dict[category]
            return
        else:
            # API
            url = 'http://mahdiemadi.ir/support_open_category' 

            params = {'variable': self.category_dict[category]}

            try:
                response = requests.get(url, params=params, timeout=2)            
            except:
                print('No conn')
                return

            results = response.json()

            results = sorted(results, key=lambda x: x[2])
            result_tuples = []
            self.product_code_DKP = {}
            max_counter = 0

            for row in results:
                                
                counter = max_counter + 1
                max_counter = counter
                
                counter_str = str(counter)
                image_path = 'http://mahdiemadi.ir/Products/%s/%s-0-v_200-h_200-q_90.jpg'%(row[0], row[0])
                color = [1, 0, 0, 1]
                font_text = '[font=font/IRANSansXFaNum-Medium.ttf]%s[/font]' % row[1]
                date_text = (row[2].split('-'))[0] + '-' + (row[2].split('-'))[1]
                other_data = tuple(row[3:])

                self.product_code_DKP[date_text] = row[0]

                #1637333-0-v_200-h_200-q_90.jpg
                item = (
                    counter_str + "-       [color=#FFFFFF].[/color]",
                    (image_path, color, font_text),
                    date_text,
                ) + other_data
                
                result_tuples.append(item)

            result_tuples = sorted(result_tuples, key=lambda x: int(x[0].split('-')[0]))

            self.data_tables = MDDataTable(
                effect_cls= 'ScrollEffect',
                use_pagination=True,
                rows_num= 10,
                elevation=2,
                size_hint_y= 1,
                pos_hint= {'center_x': .5},
                column_data=
                [   ("No.", dp(.1)),
                    ("Title", dp(45) ),#, self.sort_on_signal),
                    ("           Code", dp(5) ),
                    ("      [size=15]Avg. stock[/size]", dp(9) ),
                    ("      Min. price", dp(12) ),
                    ("      [size=15]Disc.(%)[/size]", dp(9) ),#, self.sort_on_schedule),
                    ("           [size=15]Disc. price[/size]", dp(12) ),#, self.sort_on_team),
                ],
                row_data= result_tuples, 
                #on_row_press=self.view_row_details

            )
            self.data_tables.bind(on_row_press=self.on_row_press)
            #self.data_tables.bind(on_check_press=self.on_check_press)

            self.screen = Product_table(name= '%s'%(self.category_dict[category]))
            self.screen.ids._Product_table_MDBoxLayout.add_widget(self.data_tables)
            self.screen.ids._Product_table_MDTopAppBar.title = 'Product Manager / %s'%(category)
            self.desktop_view.ids._Product.add_widget(self.screen)
            self.desktop_view.ids._Product.current = self.category_dict[category]

    def back_Product_first(self, *arg):
        self.desktop_view.ids._Product.current = 'Product_first'
        #self.desktop_view.ids._Product.ids._Product_table.ids._Product_table_MDBoxLayout.remove_widget(self.desktop_view.ids._Product.ids._Product_table.ids._Product_table_MDBoxLayout.children[0])

    def on_row_press(self, table_widget, row_data):

        self.desktop_view.ids._Product.current = 'Product_detail' 

        self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Gr.clear_widgets()
        widget_ = widget_to_delete = self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Box
        if len(widget_.children) > 1:
            widget_to_delete = self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Box.children[0]
            print(widget_to_delete)
            self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Box.remove_widget(widget_to_delete) 

        cols_num = len(table_widget.column_data)

        # Index of cell in 7 * 10 cells
        index_cell = next((index for index, obj in enumerate(row_data.parent.children) if obj == row_data), -1)

        # Find code index column with cell index
        code_index = (int(index_cell / cols_num) * cols_num + 4)

        code = row_data.parent.children[code_index].text 

        # API For get images name
        url = 'http://mahdiemadi.ir/get_image_name' 

        self.DKP = self.product_code_DKP[code]

        params = {'DKP': self.DKP}

        try:
            response = requests.get(url, params=params, timeout=2)            
        except:
            print('No conn')
            return

        results = response.json()

        images_name = sorted([item for item in results['image_files'] if len(item) <= 15])

        for item in images_name:
            self.add_image_to_Product_detail(item)

        add_pluse_image = Product_detail_image(source = 'image/add_image.jpg', icon_color= 'white', on_press= self.add_image_to_host)
        self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Gr.add_widget(add_pluse_image)

        # API for get item's information
        url = 'http://mahdiemadi.ir/get_items' 

        params = {'code': code}

        try:
            response = requests.get(url, params=params, timeout=2)            
        except:
            print('No conn')
            return

        results = response.json()

        Clock.schedule_once(partial(self.add_Box_to_Product_detail, results), 0.01)

    def add_image_to_Product_detail(self, *arg):

        code = arg[0]
        
        src = f'http://mahdiemadi.ir/Products/{self.DKP}/{code}'
       
        image = Product_detail_image(source = src)
        self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Gr.add_widget(image)

        content = image
        content.opacity = 0
        Animation(opacity = 1, duration = 1.5).start(content)

    def add_Box_to_Product_detail(self, *arg):

        add_box = Product_detail_BoxLayout(
            title= arg[0][0][0],
            code= arg[0][0][1],
            category= arg[0][0][2],
            dkp= arg[0][0][3],
            material= get_display(reshape(arg[0][0][13])),
            country= get_display(reshape(arg[0][0][14])),
            type= get_display(reshape(arg[0][0][15])),
            dt1= self.getAR(arg[0][0][16]),
            dt2= self.getAR(arg[0][0][17]),
            dt3= self.getAR(arg[0][0][18]),
            dt4= self.getAR(arg[0][0][19]),
        )
        self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Box.add_widget(add_box)

        content = add_box
        content.opacity = 0
        Animation(opacity = 1, duration = 1.5).start(content)

    def add_image_to_host(self, *arg):
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.add_image_to_host_exit_manager, select_path=self.add_image_to_host_select_path
        )
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    def add_image_to_host_exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        self.manager_open = False
        self.file_manager.close()

    def add_image_to_host_select_path(self, path: str):
        # Check if image is Ok
        check = self.add_image_to_host_is_valid_image(path)
        if check != True:
            toast(check) 
        else:
            print(path)
            toast('The image has been saved.')
            self.add_image_to_host_exit_manager()

            # Get the _Product_detail_Gr widget from the screen
            _product_detail_gr = self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Gr

            # Get the number of children widgets in _Product_detail_Gr
            num_children = len(_product_detail_gr.children)

            if num_children > 0:
   
                # Remove the last child widget from _Product_detail_Gr
                child = _product_detail_gr.children[0]
                _product_detail_gr.remove_widget(child)


            # Add image to screen
            add_image = Product_detail_image(source = path)
            self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Gr.add_widget(add_image)

            add_image = Product_detail_image(source = 'image/add_image.jpg', icon_color= 'white', on_press= self.add_image_to_host)
            self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Gr.add_widget(add_image)

            # Add image to host
            # Define the API endpoint URL
            url = 'http://mahdiemadi.ir/save_image_to_host' 

            # Image file path
            image_path = path

            # Create the payload
            payload = {
                "DKP": self.DKP
            }

            # Open the image file
            with open(image_path, "rb") as image_file:
                # Read the image file content
                image_data = image_file.read()

            # Create the files dictionary
            files = {
                "image": (image_path, image_data)
            }

            # Send the POST request to the API
            response = requests.post(url, data=payload, files=files)

            # Check the response
            if response.status_code == 200:
                print("Request successful")
            else:
                print("Request failed with status code:", response.status_code)

    def add_image_to_host_is_valid_image(*arg) -> str:
        file_path = arg[1]

        # Check if the file is an image
        try:
            image = Image.open(file_path)

        except (IOError, OSError):
            return 'The selected file is not an image.'

        # Check if the file size is under 200 KB
        file_size = os.path.getsize(file_path)
        if file_size > 200 * 1024:  # Convert 200 KB to bytes
            return 'The size of the selected image exceeds the limit.'

        # Check if the image has equal width and height
        width, height = image.size
        if width != height:
            return 'The selected image must have equal width and height.'

        return True

    def remove_image_from_host(self, *arg):
        # Remove image from screen
            # Get the _Product_detail_Gr widget from the screen
        _product_detail_gr = self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Gr

        # Get the number of children widgets in _Product_detail_Gr
        num_children = len(_product_detail_gr.children)

        if num_children > 2:
            for i in range (num_children):
                
                if arg[0] == _product_detail_gr.children[i].source:
                    child = _product_detail_gr.children[i]
                    _product_detail_gr.remove_widget(child)        
                    break
                
            # Remove image from Host
            url = 'http://mahdiemadi.ir/remove_image_from_host' 

            image_url = arg[0]  # The URL of the image to be removed

            # Define the request payload
            payload = {
                "image_url": image_url
            }

            # Send the POST request
            response = requests.post(url, data=payload)
    
    def Main_features_management_edit_action(self):
        all_widgets = self.desktop_view.ids._Product.get_screen('Product_detail').ids._Product_detail_Box.children[0].children[0].children

        for i in all_widgets:
            try: 
                if i.hint_text != 'Category' and i.hint_text != 'DKP' and i.hint_text != 'Product Code':
                    i.disabled= False
            except:
                None

    def getAR(self, arWord):
        arWord = '- ' + arWord.strip()
        if len(arWord) <= 0: return ''
        startList0 = get_display(reshape(arWord))
        # return startList0
        startList = startList0.split(' ')[::-1]
        if len(startList) == 0: return ''
        if len(startList) == 1: return str(startList[0])
        n = 110 ####################################### 55 #math.floor( w_w / f_w )
        for i in startList:
            if len(i) > n: return startList0
        tempS = ''
        resultList = []
        for i in range(0, len(startList)):
            if (tempS != ''): tempS = ' ' + tempS
            if (len(tempS) + (len(startList[i])) > n):
                tempS = tempS + "\n"
                resultList.append(tempS)
                tempS = startList[i]
            else:
                tempS = startList[i] + tempS
                if i == (len(startList)-1):
                    resultList.append(tempS)
        return ''.join(resultList)

class Test(MDApp):

    def build(self):
        Loader.loading_image = 'image/loading1.zip'
        Loader.error_image = 'image/Loader_error_image.png'
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "400"
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.accent_hue = "700"

        #self.theme_cls.theme_style = "Dark"

        return ResponsiveView() 
    
    def on_start(self):

        #cat = list(self.root.category_dict.keys())
#
        #for i in range(len(cat)):
        #    self.root.open_category_table(cat[i])

        self.root.see_orders()

Test().run()