linux kernel vulrability -> pkemn.c

It exploits a race condition in the Linux kernel’s copy-on-write (COW) mechanism for memory.

This flaw lets an unprivileged user write to read-only memory mappings.

By abusing this, the exploit can modify protected files (like /etc/passwd).

This allows the attacker to escalate privileges, typically gaining root access.

It’s a local privilege escalation vulnerability affecting many older Linux kernels.