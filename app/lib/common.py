import os

class Common():
	def __init__(self):
		pass

	def get_tag_value(self, complete_tag):
		rec_val = complete_tag.strip()
		do_copy = True
		ret_val = ""
		for ch in rec_val:
			if ch == "<":
				do_copy = False
			elif ch == ">":
				do_copy = True
			elif do_copy:
				ret_val = ret_val + ch

		return ret_val

	def get_tag_attr(self, complete_tag, attr):
		rec_val = complete_tag.strip()
		ret_val = rec_val[rec_val.find(attr):]
		ret_val = ret_val[ret_val.find('"')+1:]
		ret_val = ret_val[:ret_val.find('"')]

		return ret_val

	def make_tree(self, path):
	    tree = dict(name=os.path.basename(path), children=[])
	    try: lst = os.listdir(path)
	    except OSError:
	        pass #ignore errors
	    else:
	        for name in lst:
	            fn = os.path.join(path, name)
	            if os.path.isdir(fn):
	                tree['children'].append(make_tree(fn))
	            else:
	                tree['children'].append(dict(name=name))
	    return tree

	def update_xml_value(self, orig_xml, new_value):
		start_ind = orig_xml.find('>')
		end_ind = orig_xml.find('</')
		if end_ind > start_ind > -1 :
			orig_value = orig_xml[start_ind+1:end_ind]
			return orig_xml.replace(orig_value,new_value)
		return orig_xml

	def is_empty_tag(self, tag):
		
		if "</" in tag and not ("</config>" in tag) :
			if self.get_tag_value(tag):
				return False
			else:
				return True
		
		return False

	def find_xml_tag(self, jsdata):
		ret = []
		for item in jsdata:
			ret.append(item)
			if 'sub_options' in jsdata[item]:
				for xml_tag in self.find_xml_tag(jsdata[item]['sub_options']):
					ret.append(xml_tag)
		return ret
	
	def find_tab_items(self, tabdata, xmldoc):
		ret = []
		for item in tabdata:
			xml_tag_value = ""
			sub_item = []
			if "sub_options" in tabdata[item]:
				for sub_list_item in self.find_tab_items(tabdata[item]["sub_options"], xmldoc):
					sub_item.append(sub_list_item)
			
			if item in xmldoc:
				xml_tag_value = xmldoc[item]

			reverce_select = "false"
			if "reverce_select" in tabdata[item] and tabdata[item]["reverce_select"]:
				reverce_select = "true"


			ret_item = dict(title=tabdata[item]["caption"],
				value=xml_tag_value,
				size=tabdata[item]["size"],
				name=item,
				type=tabdata[item]["type"],
				sub_item=sub_item,
				reverce_select=reverce_select)
			
			ret.append(ret_item)

		return ret

	def make_ret_html_for_editor(self, tab_item):
		ret_html = ""
		for items in tab_item:
			ret_html = ret_html + """
			<div class='tab_item'> %s:
			""" %(items["title"])

			if items["type"] == "bool":
				check_str = ""
				if items["value"] == '1':
					check_str = "checked"
				ret_html = ret_html + """
				<input type="hidden" name="%s" value="%s"><input type="checkbox" %s id="%s" 
				onchange="this.previousSibling.value=1-this.previousSibling.value;toggleStatus(id, %s)">
				""" %(items["name"], items["value"], check_str, items["name"], items["reverce_select"])

			elif items["type"] in ["text", "number"]:
				ret_html = ret_html + """
				<input type="%s" value="%s" style="width:%spx" name="%s">
				""" %(items["type"], items["value"], items["size"], items["name"])

			if items["sub_item"]:
				
				ret_html = ret_html + """
				<div id="%s_div">
				%s
				</div>
				
				""" %(items["name"] , self.make_ret_html_for_editor(items["sub_item"]))
				
				if items["type"] != "title":
					ret_html = ret_html + """
					<script type="text/javascript">
						toggleStatus("%s", %s);
					</script>
					""" %(items["name"], items["reverce_select"])

			ret_html = ret_html + "</div>"

		return ret_html