#include <stdio.h>
#include "common.h"

#define ASIZE 2048
#define STEP  2048
#define ITERS 2048

__attribute__ ((noinline))
int loop(int zero) {
  int t = 0,i,iter;
  for(iter=0; iter < ITERS; ++iter) {
    for(i=zero; i < STEP; i+=1) {
      if(i<zero)  {
        t+=3+3*t;
      } else {
        t-=1-5*t;
      }
    }
  }
  return t;
}

int main(int argc, char* argv[]) {
   argc&=10000;
   ROI_BEGIN();
   int t=loop(argc);
   ROI_END();
   volatile int a = t;
}
