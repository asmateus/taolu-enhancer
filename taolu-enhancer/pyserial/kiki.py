from connector import Writer, Reader

c2p = Reader("C:\\Users\\academic\\taolu-enhancer\\taolu-enhancer\\Debug\\serial.exe", 1) # (pipe, conn_type)
c2p.startReading()

p2c = Writer(c2p.getProcess())
p2c.issueTimedCommand(c2p, 10) # (reader, interval)