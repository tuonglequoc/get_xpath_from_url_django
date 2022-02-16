from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import ChromeOptions as Options

from .config import TAGS, ATTRIBUTES_PRIORITY, SHOW_HIDDEN_ELEMENTS


# Chrome option
options = Options()
options.add_argument("--headless")


def get_data_from_url_by_chromedriver(url: str):
    # using chrome driver to get html source
    driver = webdriver.Chrome("chromedriver", chrome_options=options)
    driver.get(url)
    content = driver.page_source
    driver.close()
    return content


def get_bs_data(html_text: str):
    # parse to BeautifulSoup
    return bs(html_text, "html.parser")


def get_xpath(soup: bs):
    result = []

    # loop through tags need to get
    for tag in TAGS:
        elements = soup.find_all(tag)
        
        for element in elements:
            # check visibility of element
            if not SHOW_HIDDEN_ELEMENTS and not is_visible(element):
                continue

            # init first value
            element_result = {}
            xpath = f"//{tag}"

            # special case for radio button, always using "name" attribute for xpath
            if tag == "input" and element.get("type") == "radio" and element.has_attr("name"):
                # complete xpath
                xpath += "[@{}='{}']".format("name", element["name"])
            else:
                # other cases should follow the ATTRIBUTES_PRIORITY
                for attr in ATTRIBUTES_PRIORITY:
                    # check if element has attribute
                    if element.has_attr(attr):
                        value = element[attr]

                        # list will be shown as "value1 value2 value3 ..."
                        if type(value) is list:
                            value = " ".join(value)

                        # complete xpath then break the loop
                        xpath += "[@{}='{}']".format(attr, value)
                        break

            # assign to result
            element_result["xpath"] = xpath
            element_result["attributes"] = element.attrs

            # convert class list to "class1 class2 class3 ..."
            class_attr = element_result["attributes"].get("class")
            if (class_attr and isinstance(class_attr, list)):
                element_result["attributes"]["class"] = " ".join(class_attr)

            # append result
            result.append(element_result)

    # get all radio elements
    radio_elements = [ element for element in result if element["attributes"].get("type") == "radio" ]

    # exclude radio elements from the result
    result = [ element for element in result if element["attributes"].get("type") != "radio" ]

    # append combined radio elements
    result += combine_radio_button(radio_elements)

    return result


def get_title(soup: bs):
    # get page title
    title = soup.find("title")
    return title.get_text()

def is_visible(tag):
    # loads the style attribute of the element
    style = tag.attrs.get('style', False)

    # checks if the element is hidden
    if style and ('hidden' in style or 'display: none' in style or 'display:none' in style):
        return False

    # makes a recursive call to check the parent as well
    parent = tag.parent
    if parent and not is_visible(parent):
        return False

    # neither the element nor its parent(s) are hidden, so return True
    return True

def combine_radio_button(radio_elements):
    # combine radio buttons having the same xpath into one

    combined_radio_elements = []

    while radio_elements and len(radio_elements) > 0:
        tmp = radio_elements[0]

        # combine values of radio buttons having same xpath into a value list
        tmp["attributes"]["value"] = [ element["attributes"].get("value") for element in radio_elements if tmp["xpath"] == element["xpath"] ]

        # append to the result
        combined_radio_elements.append(tmp)

        # exclude processed elements
        radio_elements = [ element for element in radio_elements if tmp["xpath"] != element["xpath"] ]

    return combined_radio_elements
    