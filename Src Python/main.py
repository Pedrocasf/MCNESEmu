import threading, time, sys, pygame
sys.setrecursionlimit(2147483647)
from memory import Memory
from central_processing_unit import CPU
from picture_processing_unit import PPU
from audio_processing_unit import APU
mem = Memory()


def initialize():
    with open(sys.argv[1], mode="rb") as f:
        data = f.read()
    mapper = ((data[0x6] & 0b11110000) >> 4) | ((data[0x7]) & 0b11110000)
    mem.load_data(data, mapper, 0x4000)


initialize()
cpu = CPU()
ppu = PPU()
apu = APU()
cpu.Reset()
ppu.decode()

def test_input():
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.KEYDOWN:			
			if event.key == pygame.K_a:
				ppu.JOY1 |= 0b10000000 
			elif event.key == pygame.K_b:
				ppu.JOY1 |= 0b01000000 
			elif event.key == pygame.K_LCTRL:
				ppu.JOY1 |= 0b00100000 
			elif event.key == pygame.K_RCTRL:
				ppu.JOY1 |= 0b00010000 
			elif event.key == pygame.K_UP:
				ppu.JOY1 |= 0b00001000 
			elif event.key == pygame.K_DOWN:
				ppu.JOY1 |= 0b00000100 
			elif event.key == pygame.K_LEFT:
				ppu.JOY1 |= 0b00000010 
			elif event.key ==  pygame.K_RIGHT:
				ppu.JOY1 |= 0b00000001
				print(ppu.JOY1)

        
def cycle():
	cpu.cycles_left = 81840
	ppu.nmi_to_happen = True
	while cpu.cycles_left > 0:
		cpu.opcode_table[mem.memory[cpu.program_counter]]()
	cpu.cycles_left = 6820
	ppu.enter_VBlank()
	while cpu.cycles_left > 0:
		if (ppu.PPUCTRL & 0b10000000) == 0b10000000 and ppu.nmi_to_happen:
			ppu.nmi_to_happen = False
			cpu.NMI()
		cpu.opcode_table[mem.memory[cpu.program_counter]]()
	ppu.render_frame()
	cycle()
cycle()

