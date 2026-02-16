from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, DNS, DNSQR
from datetime import datetime

def pretty(pkt):
    ts = datetime.now().strftime("%H:%M:%S")

    if pkt.haslayer(ARP):
        a = pkt[ARP]
        op = "who-has" if a.op == 1 else "is-at" if a.op == 2 else str(a.op)
        return f"{ts}  ARP   {op:7} {a.psrc:15} -> {a.pdst:15}  {a.hwsrc}"

    if pkt.haslayer(IP):
        ip = pkt[IP]

        if pkt.haslayer(TCP):
            t = pkt[TCP]
            flags = t.sprintf("%flags%")
            return f"{ts}  TCP   {ip.src}:{t.sport:<5} -> {ip.dst}:{t.dport:<5}  flags={flags:<8} len={len(pkt)}"

        if pkt.haslayer(UDP):
            u = pkt[UDP]
            if pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
                qname = pkt[DNSQR].qname.decode(errors="ignore").rstrip(".")
                return f"{ts}  UDP   DNS     {ip.src}:{u.sport:<5} -> {ip.dst}:{u.dport:<5}  q={qname}"
            return f"{ts}  UDP          {ip.src}:{u.sport:<5} -> {ip.dst}:{u.dport:<5}  len={len(pkt)}"

        if pkt.haslayer(ICMP):
            ic = pkt[ICMP]
            return f"{ts}  ICMP         {ip.src:15} -> {ip.dst:15}  type={ic.type} code={ic.code}"

        return f"{ts}  IP           {ip.src:15} -> {ip.dst:15}  len={len(pkt)}"

    return f"{ts}  {pkt.summary()}"

print("Sniffer démarré (Ctrl+C pour arrêter)")
print("TIME      TYPE  DETAILS")
print("-"*90)

sniff(prn=lambda p: print(pretty(p)), store=False)
