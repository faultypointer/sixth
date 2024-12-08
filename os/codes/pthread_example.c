#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_THREADS 10

void *print_hello(void *tid) {
  printf("Hello from thread %p\n", tid);
  pthread_exit(NULL);
}

int main() {
  pthread_t threads[NUM_THREADS];

  for (int i = 0; i < NUM_THREADS; i++) {
    printf("Main Thread: creating thread %d\n", i);
    int status = pthread_create(&threads[i], NULL, print_hello, (void *)i);

    if (status != 0) {
      printf("Failed to create thread with error code: %d", status);
      return EXIT_FAILURE;
    }
  }
  return EXIT_SUCCESS;
}
