Title: Using strace to debug high CPU on java
Date: 2016-09-07 11:09
Author: Thanh
Category: SysAdmin
Tags: strace, cpu, java, tomcat, memory
Slug: strace-java-cpu
Status: draft

strace output from process using 100% cpu

```
root@tomcat1-prd-moogi:/var/log/tomcat8# strace -c -p 12194
strace: Process 12194 attached
^Cstrace: Process 12194 detached
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
100.00   16.934431        8596      1970       165 futex
  0.00    0.000010           0       785           sched_yield
  0.00    0.000000           0       779           mprotect
  0.00    0.000000           0         4           madvise
------ ----------- ----------- --------- --------- ----------------
100.00   16.934441                  3538       165 total
```

- Trigerring a thread dump with kill -3 also showed a lot of waiting on locks.
- Both madvise and mprotect are system calls relating to memory.
- You can also see futex has quite a high error rate.

Example output from a healthy process after adding more memory:

```
root@tomcat1-prd-moogi:/var/log/tomcat8# strace -c -p 12023
strace: Process 12023 attached
^Cstrace: Process 12023 detached
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 55.85    0.172000        2293        75         4 futex
 34.25    0.105462           0   1548087    147918 lstat
  9.09    0.028000       28000         1         1 restart_syscall
  0.81    0.002492           0     32880     30291 stat
  0.00    0.000000           0         3           write
  0.00    0.000000           0         9           open
  0.00    0.000000           0         9           close
  0.00    0.000000           0         9           fstat
  0.00    0.000000           0         2           rt_sigreturn
  0.00    0.000000           0       336           access
  0.00    0.000000           0        18           getdents
------ ----------- ----------- --------- --------- ----------------
100.00    0.307954               1581429    178214 total
```

Note:

- no madvise/mprotect
- futex has a much lower error count

Links:
http://hokstad.com/5-simple-ways-to-troubleshoot-using-strace
