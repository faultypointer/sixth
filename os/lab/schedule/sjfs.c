#include <stdio.h>

int main() {
  int p[20], bt[20], wt[20], tat[20], i, n, k, temp;
  float wtavg, tatavg;
  printf("\nEnter the number of process: ");
  scanf("%d", &n);
  for (i = 0; i < n; i++) {
    p[i] = i;
    printf("\nEnter Brust time for proces %d: ", i);
    scanf("%d", &bt[i]);
  }

  // sort by bt
  for (i = 0; i < n; i++) {
    for (k = i + 1; k < n; k++) {
      if (bt[i] > bt[k]) {
        temp = bt[i];
        bt[i] = bt[k];
        bt[k] = temp;

        temp = p[i];
        p[i] = p[k];
        p[k] = temp;
      }
    }
  }

  wt[0] = 0;
  wtavg = 0;
  tat[0] = 0;
  tatavg = 0;

  for (i = 1; i < n; i++) {
    wt[i] = wt[i - 1] + bt[i - 1];
    tat[i] = wt[i] + bt[i];
    wtavg = wtavg + wt[i];
    tatavg = tatavg + tat[i];
  }

  printf("\n\tPROCESS\t\tBURST TIME\tWAITING TIME\tTURNAROUND TIME\n");
  for (i = 0; i < n; i++) {
    printf("\tP%d\t\t%d\t\t%d\t\t%d\n", i, bt[i], wt[i], tat[i]);
  }
  printf("\nAverage Waiting Time: %f\n", wtavg / n);
  printf("\nAverage Turnaround time: %f\n", tatavg / n);
  return 0;
}
