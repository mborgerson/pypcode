#!/usr/bin/env python
# Based on sleighexample.cc
import sys
import logging
from pypcode import *

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(name)s:%(levelname)s] %(message)s')

def main():
  if len(sys.argv) != 2:
    sys.stderr.write("USAGE:  " + sys.argv[0] + " disassemble\n")
    sys.stderr.write("        " + sys.argv[0] + " pcode\n")
    sys.exit(2);
  action = sys.argv[1]

  # These are the bytes for an example x86 binary
  # These bytes are loaded at address 0x80483b4
  code = bytearray([
    0x8d, 0x4c, 0x24, 0x04, 0x83, 0xe4, 0xf0, 0xff, 0x71, 0xfc, 0x55,
    0x89, 0xe5, 0x51, 0x81, 0xec, 0xb4, 0x01, 0x00, 0x00, 0xc7, 0x45, 0xf4,
    0x00, 0x00, 0x00, 0x00, 0xeb, 0x12, 0x8b, 0x45, 0xf4, 0xc7, 0x84,
    0x85, 0x64, 0xfe, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x83, 0x45, 0xf4,
    0x01, 0x83, 0x7d, 0xf4, 0x63, 0x7e, 0xe8, 0xc7, 0x45, 0xf4, 0x02,
    0x00, 0x00, 0x00, 0xeb, 0x28, 0x8b, 0x45, 0xf4, 0x01, 0xc0, 0x89, 0x45,
    0xf8, 0xeb, 0x14, 0x8b, 0x45, 0xf8, 0xc7, 0x84, 0x85, 0x64, 0xfe,
    0xff, 0xff, 0x01, 0x00, 0x00, 0x00, 0x8b, 0x45, 0xf4, 0x01, 0x45, 0xf8,
    0x83, 0x7d, 0xf8, 0x63, 0x7e, 0xe6, 0x83, 0x45, 0xf4, 0x01, 0x83,
    0x7d, 0xf4, 0x31, 0x7e, 0xd2, 0xc7, 0x04, 0x24, 0x40, 0x85, 0x04, 0x08,
    0xe8, 0x9c, 0xfe, 0xff, 0xff, 0xc7, 0x45, 0xf4, 0x02, 0x00, 0x00,
    0x00, 0xeb, 0x25, 0x8b, 0x45, 0xf4, 0x8b, 0x84, 0x85, 0x64, 0xfe, 0xff,
    0xff, 0x85, 0xc0, 0x75, 0x13, 0x8b, 0x45, 0xf4, 0x89, 0x44, 0x24,
    0x04, 0xc7, 0x04, 0x24, 0x47, 0x85, 0x04, 0x08, 0xe8, 0x62, 0xfe, 0xff,
    0xff, 0x83, 0x45, 0xf4, 0x01, 0x83, 0x7d, 0xf4, 0x63, 0x7e, 0xd5,
    0x81, 0xc4, 0xb4, 0x01, 0x00, 0x00, 0x59, 0x5d, 0x8d, 0x61, 0xfc, 0xc3,
    0x90, 0x90, 0x90, 0x90, 0x55, 0x89, 0xe5, 0x5d, 0xc3, 0x8d, 0x74,
    0x26, 0x00, 0x8d, 0xbc, 0x27, 0x00, 0x00, 0x00, 0x00, 0x55, 0x89, 0xe5,
    0x57, 0x56, 0x53, 0xe8, 0x5e, 0x00, 0x00, 0x00, 0x81, 0xc3, 0xa5,
    0x11, 0x00, 0x00, 0x83, 0xec, 0x1c, 0xe8, 0xd7, 0xfd, 0xff, 0xff, 0x8d,
    0x83, 0x20, 0xff, 0xff, 0xff, 0x89, 0x45, 0xf0, 0x8d, 0x83, 0x20,
    0xff, 0xff, 0xff, 0x29, 0x45, 0xf0, 0xc1, 0x7d, 0xf0, 0x02, 0x8b, 0x55,
    0xf0, 0x85, 0xd2, 0x74, 0x2b, 0x31, 0xff, 0x89, 0xc6, 0x8d, 0xb6,
    0x00, 0x00, 0x00, 0x00, 0x8b, 0x45, 0x10, 0x83, 0xc7, 0x01, 0x89, 0x44,
    0x24, 0x08, 0x8b, 0x45, 0x0c, 0x89, 0x44, 0x24, 0x04, 0x8b, 0x45,
    0x08, 0x89, 0x04, 0x24, 0xff, 0x16, 0x83, 0xc6, 0x04, 0x39, 0x7d, 0xf0,
    0x75, 0xdf, 0x83, 0xc4, 0x1c, 0x5b, 0x5e, 0x5f, 0x5d, 0xc3, 0x8b,
    0x1c, 0x24, 0xc3, 0x90, 0x90, 0x90, 0x55, 0x89, 0xe5, 0x53, 0xbb, 0x50,
    0x95, 0x04, 0x08, 0x83, 0xec, 0x04, 0xa1, 0x50, 0x95, 0x04, 0x08,
    0x83, 0xf8, 0xff, 0x74, 0x0c, 0x83, 0xeb, 0x04, 0xff, 0xd0, 0x8b, 0x03,
    0x83, 0xf8, 0xff, 0x75, 0xf4, 0x83, 0xc4, 0x04, 0x5b, 0x5d, 0xc3,
    0x55, 0x89, 0xe5, 0x53, 0x83, 0xec, 0x04, 0xe8, 0x00, 0x00, 0x00, 0x00,
    0x5b, 0x81, 0xc3, 0x0c, 0x11, 0x00, 0x00, 0xe8, 0x00, 0xfe, 0xff,
    0xff, 0x59, 0x5b, 0xc9, 0xc3, 0x03, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x50, 0x72, 0x69, 0x6d, 0x65, 0x73,
    0x00, 0x25, 0x64, 0x0a, 0x00, 0x00
    ])

  start = 0x80483b4
  stop = 0x804846c

  log.debug('Loading image')
  loader = SimpleLoadImage(start, code, len(code))

  # Set up the context object
  log.debug('Creating context')
  context = ContextInternal()

  # Set up the assembler/pcode-translator
  log.debug('Setting up translator')
  sleighfilename = os.path.join(SLEIGH_SPECFILES_PATH, 'x86', 'data', 'languages', 'x86.sla')
  trans = Sleigh(loader, context)

  log.debug('Reading Sleigh file into DOM')
  docstorage = DocumentStorage()

  log.debug('Opening document')
  doc = docstorage.openDocument(sleighfilename).getRoot()

  log.debug('Registering tags')
  docstorage.registerTag(doc)

  log.debug('Initializing translator')
  trans.initialize(docstorage) # Initialize the translator
  log.debug('Ok')

  # Now that context symbol names are loaded by the translator
  # we can set the default context
  context.setVariableDefault("addrsize",1) # Address size is 32-bit
  context.setVariableDefault("opsize",1) # Operand size is 32-bit

  emit = PcodeRawOutHelper(trans) # Set up the pcode dumper
  asm = AssemblyEmitCacher() # Set up the disassembly dumper
  addr = Address(trans.getDefaultCodeSpace(), start) # First address to translate
  lastaddr = Address(trans.getDefaultCodeSpace(), stop) # Last address

  if action == "disassemble":
    while addr < lastaddr:
      # Disassemble an instruction
      length = trans.printAssembly(asm, addr)
      print('%08x: %s %s' % (asm.addr.getOffset(), asm.mnem, asm.body))
      addr = addr + length # Advance to next instruction

  elif action == "pcode":
    def print_vardata(data):
      sys.stdout.write('(%s, 0x%x, %d) ' % (data.space.getName(), data.offset, data.size))
      if data.space.getName() == 'register':
        regname = trans.getRegisterName(data.space, data.offset, data.size)
        sys.stdout.write('{%s} ' % regname)

    while addr < lastaddr:
      emit.clearCache()
      trans.printAssembly(asm, addr) # Disassemble this instruction
      print('%08x: %s %s' % (asm.addr.getOffset(), asm.mnem, asm.body))
      length = trans.oneInstruction(emit, addr) # Translate instruction to pcode
      for op in emit.opcache:
        out = op.getOutput()
        if out:
          print_vardata(out)
          sys.stdout.write('= ')
        sys.stdout.write('%s ' % get_opname(op.getOpcode()))
        for i in range(op.numInput()):
          print_vardata(op.getInput(i))
        sys.stdout.write('\n')

      sys.stdout.write('\n')
      addr = addr + length # Advance to next instruction
  else:
    sys.stdout.write("Unknown action: " + action + "\n")

if __name__ == '__main__':
	main()
