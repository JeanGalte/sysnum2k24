#include <stdio.h>
#include <time.h>

int main(void) {
    time_t rtime = time(NULL);
    struct tm *ptm = localtime(&rtime);
    /*
      Année : ptm->tm_year+1900
      Mois : ptm->tm_mon+1
      Jour du mois : ptm->tm_mday
      Heure : ptm->tm_hour
      Minutes : ptm->tm_min
      Secondes : ptm->tm_sec
     */

    /* Exemple */
    /* printf("The time is: %02d:%02d:%02d:%02d:%02d:%02d\n", */
    /* 	   ptm->tm_year + 1900, */
    /* 	   ptm->tm_mday, */
    /* 	   ptm->tm_mon+1, */
    /* 	   ptm->tm_hour, */
    /*        ptm->tm_min, */
    /* 	   ptm->tm_sec); */
    /* return 0 */;
}
