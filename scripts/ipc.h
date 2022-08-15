/* This head file defines macros that start and end tracking the counters
 * for cycles and instructions on a RISC-V system. Any program using this
 * head file must be compiled with -std=gnu<any_year> and without compiler
 * optimization flags. Any binary using this header must be run with
 * taskset to fix it to a core. Otherwise, the binary may get context switched
 * to a different core that has different counter values. The user that runs
 * the binary must have permissions to read the cycle and instruction counters.
 */

#ifndef IPC_H
#define IPC_H

#include <stdio.h>

/* gather initial cycle and instruction counts */
#define IPC_BEGIN() \
    register unsigned long long int t3 asm("t3"); \
    __asm__ __volatile__ ("rdcycle t3"); \
    unsigned long long int cycles_i = t3; \
    __asm__ __volatile__ ("rdinstret t3"); \
    unsigned long long int inst_commit_i = t3;

/* gather final cycle and instruction counts and print the results */
#define IPC_END() \
    __asm__ __volatile__ ("rdcycle t3"); \
    unsigned long long int cycles_f = t3; \
    __asm__ __volatile__ ("rdinstret t3"); \
    unsigned long long int inst_commit_f = t3; \
    unsigned long long int cycles = cycles_f - cycles_i; \
    unsigned long long int inst_commit = inst_commit_f - inst_commit_i; \
    double ipc = (float) inst_commit / cycles; \
    printf("cycles = %llu\n", cycles); \
    printf("instructions committed = %llu\n", inst_commit); \
    printf("IPC = %lf\n", ipc); \
    printf("CPI = %lf\n", 1 / ipc);

#endif

