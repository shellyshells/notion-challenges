## 🗂️ File Structure

```
arrakis_chapters/
├── README.md (this file)
├── chapter_02_ssh.py
├── chapter_03_tempfiles.py
├── chapter_04_icmp.py
├── chapter_05_server.py
├── chapter_05_client.py
├── chapter_06_argparse.py
├── chapter_07_signals.py
├── chapter_08_subprocess.py
├── chapter_09_http.py
├── chapter_10_activity_report.py
├── chapter_11_scapy_sniffer.py
├── chapter_12_multiprocessing.py
├── chapter_13_email.py
├── chapter_15_preparation.py
├── chapter_17_reverse_shell.py
├── chapter_20_malware_showcase.py
├── chapter_24_keylogger.py
└── chapter_26_mac_changer.py
```

---

## 📚 Chapters Overview

### Chapter 1: Préparation
**Status:** Setup only (no code required)  
**Tasks:** Character setup, VM configuration, Python installation

### Chapter 2: SSH Connection
**File:** `chapter_02_ssh.py`  
**Concepts:** SSH connectivity using Spur library, remote command execution  
**Key Learning:** Network authentication, secure remote access

### Chapter 3: Temporary Files
**File:** `chapter_03_tempfiles.py`  
**Concepts:** `tempfile` module, secure file handling, automatic cleanup  
**Key Learning:** Temporary file management, security best practices

### Chapter 4: ICMP Dissection
**File:** `chapter_04_icmp.py`  
**Concepts:** Scapy packet creation, ICMP protocol, network diagnostics  
**Key Learning:** Packet crafting, network layer protocols

### Chapter 5: Socket Programming
**Files:** `chapter_05_server.py`, `chapter_05_client.py`  
**Concepts:** TCP sockets, client-server architecture, multithreading  
**Key Learning:** Network programming fundamentals, concurrent connections

### Chapter 6: Command-Line Arguments
**File:** `chapter_06_argparse.py`  
**Concepts:** `argparse` module, CLI design, parameter validation  
**Key Learning:** Professional command-line interface creation

### Chapter 7: Signal Interception
**File:** `chapter_07_signals.py`  
**Concepts:** Signal handling, SIGINT, graceful shutdown  
**Key Learning:** Process signals, interrupt handling

### Chapter 8: Process Management
**File:** `chapter_08_subprocess.py`  
**Concepts:** `subprocess` module, external command execution, MySQL interaction  
**Key Learning:** Process spawning, database integration via CLI

### Chapter 9: HTTP Requests
**File:** `chapter_09_http.py`  
**Concepts:** `requests` library, REST APIs, HTTP methods  
**Key Learning:** Web communication, API interaction

### Chapter 10: Activity Report
**File:** `chapter_10_activity_report.py`  
**Concepts:** SAR data parsing, data visualization with Matplotlib  
**Key Learning:** System monitoring, performance analysis

### Chapter 11: Network Sniffing
**File:** `chapter_11_scapy_sniffer.py`  
**Concepts:** Packet capture with Scapy, traffic analysis, BPF filters  
**Key Learning:** Network monitoring, protocol analysis

### Chapter 12: Multiprocessing
**File:** `chapter_12_multiprocessing.py`  
**Concepts:** `multiprocessing` module, parallel execution, process management  
**Key Learning:** Concurrent programming, CPU utilization

### Chapter 13: Email
**File:** `chapter_13_email.py`  
**Concepts:** SMTP protocol, email sending with `smtplib`  
**Key Learning:** Email automation, SMTP configuration

### Chapter 15: Preparation (Phase 2)
**File:** `chapter_15_preparation.py`  
**Concepts:** Environment verification for advanced chapters  
**Key Learning:** System requirements checking

### Chapter 17: Reverse Shell
**File:** `chapter_17_reverse_shell.py`  
**Concepts:** Remote shell, SSH directory listing, system control  
**Key Learning:** Remote access techniques (educational only!)

### Chapter 20: Malware Showcase
**File:** `chapter_20_malware_showcase.py`  
**Concepts:** Malware analysis, repository cloning, code inspection  
**Key Learning:** Security awareness, threat analysis

### Chapter 24: Keylogger
**File:** `chapter_24_keylogger.py`  
**Concepts:** Keyboard monitoring with `pynput`, event handling  
**Key Learning:** Input capture techniques (educational only!)

### Chapter 26: MAC Address Changer
**File:** `chapter_26_mac_changer.py`  
**Concepts:** Network interface manipulation, MAC address modification  
**Key Learning:** Network configuration, interface management


sudo python3 chapter_11_scapy_sniffer.py
sudo python3 chapter_26_mac_changer.py
```

### Getting Help
All scripts support the `-h` or `--help` flag:
```bash
python3 chapter_XX_name.py --help
```

---


### Chapters Requiring Special Care:
- Chapter 4 (ICMP) - Requires network access
- Chapter 11 (Sniffer) - Captures all network traffic
- Chapter 17 (Reverse Shell) - Remote access tool
- Chapter 20 (Malware) - Contains malicious code samples
- Chapter 24 (Keylogger) - Privacy implications
- Chapter 26 (MAC Changer) - Network configuration changes



## 📖 References & Resources

- **Python Documentation:** https://docs.python.org/3/
- **Scapy Documentation:** https://scapy.readthedocs.io/
- **Requests Library:** https://requests.readthedocs.io/
- **Socket Programming:** https://docs.python.org/3/library/socket.html
- **Argparse Tutorial:** https://docs.python.org/3/howto/argparse.html

---

## 🏆 Completion Status

**Total: (ALL) 18 Chapters Completed** 
