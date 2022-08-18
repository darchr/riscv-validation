#ifndef COMMON_H
#define COMMON_H

#ifdef FF //Ignore this.
#include <stdlib.h>

#define ROI_BEGIN() \
  __asm__ __volatile__(".byte 0x0f\n\t.byte 0x27\n\t.byte 0x00\n\t.byte 0x0b")
#define ROI_END() \
  exit(0)
  //_exit(0)

#elif MAGIC //current default

//Magic only works for X86 right now
#define ROI_BEGIN() \
  __asm__ __volatile__ ("xchg %bx,%bx");
#define ROI_END() \
  __asm__ __volatile__ ("xchg %cx,%cx");


#define DETAILED_SIM_STOP() \
    _exit(0)
#else // Ignore this for now -- put working timing code here
#include <stdlib.h>
#define ROI_BEGIN()
#define ROI_END() \
    exit(0)

#endif // NO MAGIC

#endif //define COMMON_H
