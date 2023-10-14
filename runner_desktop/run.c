#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void * runner_server(void * args){
    pthread_mutex_lock(&mutex);
    system("cd ~");
    chdir("/home/lypess/Documentos/eye_tracking_app/server");
    pthread_mutex_unlock(&mutex);
    system("python server_script.py");
}
void * runner_opencv(void * args){
    pthread_mutex_lock(&mutex);
    system("cd ~");
    chdir("/home/lypess/Documentos/eye_tracking_app//backend/src");
    pthread_mutex_unlock(&mutex);
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