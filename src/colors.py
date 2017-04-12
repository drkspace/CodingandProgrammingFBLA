#(c)Daniel Robert Kramer,2017. All Rights Reseved
from enum import Enum

#Using googles color palets
#Found at https://material.io/guidelines/style/color.html#color-color-palette

class theme(Enum):
	none = 0
	light = 1
	dark = 2
	red = 3
	pink  = 4
	purple = 5
	deep_purple = 6
	indigo = 7
	blue = 8
	light_blue = 9
	cyan = 10
	teal = 11
	green = 12
	light_green = 13
	lime = 14
	yellow = 15
	amber = 16
	orange = 17
	deep_orange = 18
	brown = 19
	grey = 20
	blue_grey = 21

class colors(object):
	
	def __init__(self):
		self.background = "#000000"
		self.accent = "#000000"
		self.entry = "#000000"
		self.table_background = "#000000"
		self.text_color = "#000000"
		self.theme = theme(0)
		
	
	def set_color_theme(self, atheme):
		
		self.theme = atheme

		if atheme == theme.light:
			self.background = "#FAFAFA"
			self.accent = "#F5F5F5"
			self.entry = "#FFFFFF"
			self.table_background = "#E0E0E0"
			self.text_color = "#000000"

		elif atheme == theme.dark:
			self.background = "#303030"
			self.accent = "#212121"
			self.entry = "#000000"
			self.table_background = "#000000"
			self.text_color = "#FFFFFF"

		elif atheme == theme.red:
			self.background = "#EF5350"
			self.accent = "#FF1744"
			self.entry = "#E57373"
			self.table_background = "#E57373"
			self.text_color = "#000000"

		elif atheme == theme.pink:
			self.background = "#EC407A"
			self.accent = "#F50057"
			self.entry = "#F06292"
			self.table_background = "#F06292"
			self.text_color = "#000000"
		
		elif atheme == theme.purple:
			self.background = "#AB47BC"
			self.accent = "#D500F9"
			self.entry = "#BA68C8"
			self.table_background = "#BA68C8"
			self.text_color = "#000000"

		elif atheme == theme.deep_purple:
			self.background = "#7E57C2"
			self.accent = "#651FFF"
			self.entry = "#9575CD"
			self.table_background = "#9575CD"
			self.text_color = "#000000"
		
		elif atheme == theme.indigo:
			self.background = "#5C6BC0"
			self.accent = "#3D5AFE"
			self.entry = "#7986CB"
			self.table_background = "#7986CB"
			self.text_color = "#000000"

		elif atheme == theme.blue:
			self.background = "#42A5F5"
			self.accent = "#42A5F5"
			self.entry = "#64B5F6"
			self.table_background = "#64B5F6"
			self.text_color = "#000000"
		
		elif atheme == theme.light_blue:
			self.background = "#29B6F6"
			self.accent = "#00B0FF"
			self.entry = "#4FC3F7"
			self.table_background = "#4FC3F7"
			self.text_color = "#000000"
				
		elif atheme == theme.cyan:
			self.background = "#26C6DA"
			self.accent = "#00E5FF"
			self.entry = "#4DD0E1"
			self.table_background = "#4DD0E1"
			self.text_color = "#000000"

		elif atheme == theme.teal:
			self.background = "#26A69A"
			self.accent = "#1DE9B6"
			self.entry = "#4DB6AC"
			self.table_background = "#4DB6AC"
			self.text_color = "#000000"

		elif atheme == theme.green:
			self.background = "#66BB6A"
			self.accent = "#00E676"
			self.entry = "#81C784"
			self.table_background = "#81C784"
			self.text_color = "#000000"

		elif atheme == theme.light_green:
			self.background = "#9CCC65"
			self.accent = "#76FF03"
			self.entry = "#AED581"
			self.table_background = "#AED581"
			self.text_color = "#000000"

		elif atheme == theme.lime:
			self.background = "#D4E157"
			self.accent = "#C6FF00"
			self.entry = "#DCE775"
			self.table_background = "#DCE775"
			self.text_color = "#000000"

		elif atheme == theme.yellow:
			self.background = "#FFEE58"
			self.accent = "#FFEA00"
			self.entry = "#FFF176"
			self.table_background = "#FFF176"
			self.text_color = "#000000"

		elif atheme == theme.amber:
			self.background = "#FFCA28"
			self.accent = "#FFC400"
			self.entry = "#FFD54F"
			self.table_background = "#FFD54F"
			self.text_color = "#000000"
	
		elif atheme == theme.orange:
			self.background = "#FFA726"
			self.accent = "#FF9100"
			self.entry = "#FFB74D"
			self.table_background = "#FFB74D"
			self.text_color = "#000000"

		elif atheme == theme.deep_orange:
			self.background = "#FF7043"
			self.accent = "#FF3D00"
			self.entry = "#FF8A65"
			self.table_background = "#FF8A65"
			self.text_color = "#000000"

		elif atheme == theme.brown:
			self.background = "#8D6E63"
			self.accent = "#BCAAA4"
			self.entry = "#A1887F"
			self.table_background = "#A1887F"
			self.text_color = "#FFFFFF"

		elif atheme == theme.grey:
			self.background = "#BDBDBD"
			self.accent = "#EEEEEE"
			self.entry = "#E0E0E0"
			self.table_background = "#E0E0E0"
			self.text_color = "#000000"

		elif atheme == theme.blue_grey:
			self.background = "#78909C"
			self.accent = "#B0BEC5"
			self.entry = "#90A4AE"
			self.table_background = "#90A4AE"
			self.text_color = "#000000"
