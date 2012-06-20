.. contents::

Introduction
============

This package holds a number of transforms for Plone's portal_transforms tool that use tika to extract text from binary content like PDF or Word files. The transforms are not automatically added, you need to do that manually. The transforms have a parameter exec-prefix that can be set to the directory containing the tika executable (file name tika or tika-bin is expected). If it is not set the system path is searched.

