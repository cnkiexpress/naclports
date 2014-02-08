#!/usr/bin/env python
# Copyright (c) 2013 The Native Client Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Tool for generating list of ports in wiki format.
"""

import optparse
import os
import sys

import naclports

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NACLPORTS_ROOT = os.path.dirname(SCRIPT_DIR)
SRC_URL = 'https://code.google.com/p/naclports/source/browse/trunk/src'

options = None

def main(args):
  global options
  parser = optparse.OptionParser(description=__doc__)
  parser.add_option('-v', '--verbose', action='store_true',
                    help='Output extra information.')
  options, _ = parser.parse_args(args)
  rtn = 0

  print '#summary List of ports available in naclports.'
  print '= List of available !NaCl ports ='
  print ''
  print 'Port are listed in alphabetical order, with links to the upstream'
  print 'source archive and the patch used when building for !NaCl.'
  print 'This listing is auto-generated by the'
  print '[%s/build_tools/generate_port_list.py generate_port_list.py]' % SRC_URL
  print 'script.'
  print ''
  print '|| *Name* || *Upstream Archive* || *!NaCl Patch* ||'
  total = 0
  for package in sorted(naclports.PackageIterator()):
    if not package.URL:
      continue
    patch = os.path.join(package.root, 'nacl.patch')
    if os.path.exists(patch):
      relative_path = os.path.relpath(patch, NACLPORTS_ROOT)
      size = os.path.getsize(patch)
      if size < 1024:
        patch = '[%s/%s %d B]' % (SRC_URL, relative_path, size)
      else:
        patch = '[%s/%s %d KiB]' % (SRC_URL, relative_path, size/1024)
    else:
      patch = '_none_'
    url = '[%s %s]' % (package.URL, package.GetArchiveFilename())
    package_url = '[%s/%s %s]' % (SRC_URL,
                                  os.path.relpath(package.root, NACLPORTS_ROOT),
                                  package.PACKAGE_NAME)
    print '|| %-70s || %-70s || %s ||' % (package_url, url, patch)
    total += 1
  print '\n_Total = %d_\n' % total

  print '= Local Ports (not based on upstream sources) =\n'
  total = 0
  for package in naclports.PackageIterator():
    if package.URL:
      continue
    package_url = '[%s/%s %s]' % (SRC_URL,
                                  os.path.relpath(package.root, NACLPORTS_ROOT),
                                  package.PACKAGE_NAME)
    print '|| %-70s ||' % package_url
    total += 1
  print '\n_Total = %d_\n' % total


  return rtn

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))