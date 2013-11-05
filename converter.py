import sys
#from dicttoxml import dicttoxml    # Uncomment this to use the old converter.
from json import loads, dumps
from re import compile
from xml.dom.minidom import parseString

def unicode_to_string(unicode_obj):
  return unicode_obj.encode('utf-8')

def pretty_print(text, indent):
  print unicode_to_string((" " * indent) + text)

def print_simple(key, value, indent, attrs={}):
  if isinstance(value, unicode):
    value = compile('<.*>').sub('', value).replace('&', 'and')
  attr_str = ''
  for attr in attrs:
    attr_str += ' %s="%s"' % (attr, attrs[attr])
  pretty_print('<%s%s>%s</%s>' % (key, attr_str, value, key), indent)

def print_list(element, data, indent, spaces):
  if element == "sha":
    print_simple(element, data[0], indent)
  else:
    pretty_print('<%s>' % element, indent)
    for item in data:
      print_object(element[:-1], item, indent + spaces, spaces)
    pretty_print('</%s>' % element, indent)

def print_dict(element, data, indent, spaces):
  pretty_print('<%s>' % element, indent)
  for key in data.keys():
    print_object(key, data[key], indent + spaces, spaces)
  pretty_print('</%s>' % element, indent)

def print_object(key, value, indent, spaces):
  if value == None:
    pass
  elif isinstance(value, (bool, int, str, unicode)):
    print_simple(key, value, indent)
  elif isinstance(value, dict):
    print_dict(key, value, indent, spaces)
  elif isinstance(value, list):
    print_list(key, value, indent, spaces)
  else:
    raise ValueError

if (__name__ == '__main__') and (len(sys.argv) == 2):
  f = open(sys.argv[1])
  data = loads('[%s]' % f.read().replace('}\n{', '},\n{'))
  f.close()
  #print dumps(data, indent=2, separators=(',', ': '))    # Print data as JSON.
  try:
    xml = parseString(unicode_to_string(dicttoxml(data)))
    print unicode_to_string(xml.toprettyxml())
  except NameError:
    indent, spaces = 0, 2
    pretty_print('<?xml version="1.0" encoding="UTF-8"?>', indent)
    print_list('events', data, indent, spaces)

