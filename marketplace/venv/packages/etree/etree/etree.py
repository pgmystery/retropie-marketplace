# -*- coding: utf-8 -*-
import html5lib
import re
from xml.etree import ElementTree


def parse(doc):
	return html5lib.parse(doc, namespaceHTMLElements=False)


def prefix(element_or_tree):
	m = re.match(r'{.*\}', element_or_tree.tag)
	return m.group(0) if m else ''


def strip_elements(tree_or_element, *tag_names):
	all_elements = []
	current_prefix = prefix(tree_or_element)
	tag_names_with_prefix = []
	for tag in tag_names:
		tag_names_with_prefix.append(current_prefix + tag)

	parent_map = dict((c, p) for p in tree_or_element.iter() for c in p)

	for element in tree_or_element.iter():
		if element.tag in tag_names_with_prefix:
			all_elements.append(element)

	for element in all_elements:
		parent_map[element].remove(element)


def tostring(tree_or_element, encoding="UTF-8", method="text"):
	return ElementTree.tostring(tree_or_element, encoding=encoding, method=method)
