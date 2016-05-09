from litex.gen import *

class PhySettings:
    def __init__(self, memtype, dfi_databits,
                 nphases,
                 rdphase, wrphase,
                 rdcmdphase, wrcmdphase,
                 cl, read_latency, write_latency, cwl=0):
        self.memtype = memtype
        self.dfi_databits = dfi_databits

        self.nphases = nphases
        self.rdphase = rdphase
        self.wrphase = wrphase
        self.rdcmdphase = rdcmdphase
        self.wrcmdphase = wrcmdphase

        self.cl = cl
        self.read_latency = read_latency
        self.write_latency = write_latency
        self.cwl = cwl


class GeomSettings:
    def __init__(self, bankbits, rowbits, colbits):
        self.bankbits = bankbits
        self.rowbits = rowbits
        self.colbits =  colbits
        self.addressbits = max(rowbits, colbits)


class TimingSettings:
    def __init__(self, tRP, tRCD, tWR, tWTR, tREFI, tRFC):
        self.tRP = tRP
        self.tRCD = tRCD
        self.tWR = tWR
        self.tWTR = tWTR
        self.tREFI = tREFI
        self.tRFC = tRFC


def cmd_layout(aw):
    return [
        ("valid",        1, DIR_M_TO_S),
        ("ready",        1, DIR_S_TO_M),
        ("we",           1, DIR_M_TO_S),
        ("adr",         aw, DIR_M_TO_S),
        ("lock",         1, DIR_S_TO_M),

        ("wdata_ready",  1, DIR_S_TO_M),
        ("rdata_valid",  1, DIR_S_TO_M)
    ]


def data_layout(dw):
    return [
        ("wdata",       dw, DIR_M_TO_S),
        ("wdata_we", dw//8, DIR_M_TO_S),
        ("rdata",       dw, DIR_S_TO_M)
    ]


class LiteDRAMInterface(Record):
    def __init__(self, address_align, settings):
        self.aw = settings.geom.rowbits + settings.geom.colbits - address_align
        self.dw = settings.phy.dfi_databits*settings.phy.nphases
        self.nbanks = 2**settings.geom.bankbits
        self.settings = settings

        layout = [("bank"+str(i), cmd_layout(self.aw)) for i in range(self.nbanks)]
        layout += data_layout(self.dw)
        Record.__init__(self, layout)


class LiteDRAMPort(Record):
    def __init__(self, aw, dw):
        self.aw = aw
        self.dw = dw

        layout = cmd_layout(aw) + data_layout(dw)
        Record.__init__(self, layout)


def cmd_request_layout(a, ba):
    return [
        ("a",     a),
        ("ba",   ba),
        ("cas",   1),
        ("ras",   1),
        ("we",    1)
    ]


def cmd_request_rw_layout(a, ba):
    return cmd_request_layout(a, ba) + [
        ("is_cmd", 1),
        ("is_read", 1),
        ("is_write", 1)
    ]