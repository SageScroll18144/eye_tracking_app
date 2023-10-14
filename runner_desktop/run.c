#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

void * runner_server(void * args){
    chdir("../server/");
    system("python server_script.py");
}
void * runner_opencv(void * args){
    chdir("../backend/src");
    system("python main.py");
}

int main(){
    pthread_t th_server, th_opencv;

    pthread_create(&th_server, NULL, runner_server, NULL);
    pthread_create(&th_opencv, NULL, runner_opencv, NULL);

    pthread_join(th_server, NULL);
    pthread_join(th_opencv, NULL);

    pthread_exit(NULL);
}