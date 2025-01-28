#include <stdlib.h>
#include <ncurses.h>
#include <pthread.h>
#include <unistd.h>
#define LEN_OF_MESSAGE 29

char month_name[12][10] = {"janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"};

void printer(char *s) {
  mvprintw((LINES - 1)/2, (COLS - LEN_OF_MESSAGE)/2, s);
  refresh();
}

void *thread_printer(void *arg) {
  char *s = (char*) malloc((LEN_OF_MESSAGE+1)*sizeof(char));
  while (1) {
    sprintf(s, "%02d:%02d:%02d - %d %s %d", (int) ram_date[3], (int) ram_date[4], (int) ram_date[5], (int) ram_date[2], month_name[(int) ram_date[1]-1], (int) ram_date[0]);
    printer(s);
    usleep(15);
  }
	pthread_exit(EXIT_SUCCESS);
}

int main(void) {
    initscr();
    curs_set(0);

    pthread_t thread1;
    pthread_create(&thread1, NULL, thread_printer, NULL);

    // exécution du thread principal
    
    getch();
    endwin();
    
    return 0;
}
