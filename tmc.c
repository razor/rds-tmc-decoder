#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "tmc_events.h"

#define PI 0xC401
#define GROUP_8A 0x8000



typedef struct TMCMsg {
    int block1;
    int block2;
    int block3;
    int block4;
} TMCMsg;

TMCMsg tmcmsg;

const char * eventmsg[TMC_EVENTS];

void load_eventcode()
{
    int i;
    for (i=0; i<TMC_EVENT_LIST_LINES; i++) {
        int code = strtol(tmc_events[i][2], NULL, 10);
        if (code != 0) {
            eventmsg[code] = 
            tmc_events[i][1];
//            printf("%d=>%s\n", code, eventmsg[code]);
        }
    }
}

void parsemsg(const char *msg)
{
    char *endptr = NULL;
    tmcmsg.block1 = strtol(msg, &endptr, 16);
    tmcmsg.block2 = strtol(endptr, &endptr, 16);
    tmcmsg.block3 = strtol(endptr, &endptr, 16);
    tmcmsg.block4 = strtol(endptr, &endptr, 16);
}

const char * getevent()
{
    int mask = (1 << 11) - 1;
    int eventcode = tmcmsg.block3 & mask;
    return eventmsg[eventcode];   
}

void main()
{
    char buf[32];
    load_eventcode();
    while (fgets(buf, 32, stdin) != NULL) {
        int s = strlen(buf);
        *(buf+s-1) = 0;
        parsemsg(buf);
        if ((tmcmsg.block2 & 0xF800) == GROUP_8A && 
            (tmcmsg.block2 & 0x1F) == 0x8) printf("%s\t%s\n", buf, getevent());
        else printf("%s\t-\n", buf);
    }
}

