from file import File
from file_processor import Logger, FileProcessor
from config import Config
import xml.etree.ElementTree as ET
import pandas as pd
import csv


# TO-DO 
# Make so that it can create different csv files depending on it's content
# Select what elements get into the csv and which ones don't
# 


class XML(File):
    def __init__(self, path):
        super().__init__(path) 

    def get_tree(self):
        return ET.parse(self.path)

    def get_root_element(self):
        return ET.parse(self.path).getroot()

    def get_root_string(self):
        return ET.parse(self.path).getroot().tag

    def get_children_names(self, elementList):
        for child in elementList:
            print(child.tag)
        return

    def has_children(self, element):
        return bool(list(element))

    #Returns a list with the children of an element
    def get_children_element(self, element):
        return element.findall("./")

    def print_geneology(self, elementList, counter = 0):
        indent = "    "
        lastName = ""
        for element in elementList:
            if not element.tag == lastName:
                if counter == 0:
                    prefix = ""
                else:
                    spacing = indent * counter
                    prefix = spacing + "|-"
                print(prefix + element.tag)
                if self.has_children(element): #Implement has_children method 
                    lastName = element.tag
                    childrenList = self.get_children_element(element)
                    self.print_geneology(childrenList, counter + 1)

    def get_attribute_value(self, element, name):
        if isinstance(element, (str, int, float, list)):
            raise TypeError(f"Expected an element object, but received a primitive type: {type(element).__name__}.")
        try:
            return element.attrib[name] #maybe better element.get(name)
        except AttributeError:
            raise TypeError(f"Element has no attributes")
        except KeyError:
                # Handles cases where the attribute 'name' does not exist in element.attrib
                print(f"Element has no attribute '{name}'")
                return 


    def get_value(self, element):
        if isinstance(element, (str, int, float, list)):
            raise TypeError(f"Expected an element object, but received a primitive type: {type(element).__name__}.")
        
        try:
            if not element.text is None:
                return element.text
            else:
                print("Warning: Element has no tag value")
        except AttributeError:
            raise TypeError(f"Element has no 'tag' attribute")

    def find_value_from_tag(self, element, name):
        return element.find(name).text

    
if __name__ == "__main__":
    path = r"C:\Test\country_data.xml"
    #path = r"C:\Test\country_data.xml"
    file = XML(path)
    root = file.get_root_element()
    file.print_geneology(root)
    #print(root)
    #child = root.find("./")
    #print(child.tag)
    #print(child.attrib)
    #print(file.get_attribute_value(child, "client-name"))
    #file.get_value(child)
    #for children in child: 
    #    print(file.get_value(children))


    '''
    childrenList = root.findall("./")
    for child in childrenList:
        print(child.tag)
    root.findall(".//neighbor[2]")
    print(root.find("./country/neighbor[2]").text)
    '''