#include "IO.h"

static int random_num(int min, int max) {
    srand(time(NULL));
    int range = max - min + 1;
    return (rand() % range) + min;
}

FILE* open_or_exit(const char* filename, char* mode) {
    FILE* fp = fopen(filename, mode);
    if (fp == NULL) {
        printf("File %s could not be opened with %s mode\n", filename, mode);
        exit(1);
    }
    return fp;
}

void free_FILE_CONTENT(FILE_CONTENT* fc) {
    for (int i = 0; i < fc->num_lines; i++)
        free(fc->lines[i]);
    free(fc->lines);
}

char* get_word(const char *filename) {
    FILE *fp = open_or_exit(filename, "r");
    FILE_CONTENT filec = readlines(fp);

    int rnd_line = random_num(0, filec.num_lines);
    char *secret_word = malloc(sizeof(char) * (strlen(filec.lines[rnd_line]) + 1));
    strcpy(secret_word, filec.lines[rnd_line]);
    
    free_FILE_CONTENT(&filec);
    return secret_word;
}

FILE_CONTENT readlines(FILE *fp) {
    // Assume initial length of file
    int max_lines = 50000;

    // Assume all words are under 30 chars long
    const int MAX_LEN_WORD = 30;
    
    FILE_CONTENT fc;
    fc.lines = malloc(sizeof(char *) * max_lines);
    
    char* tmp = malloc(sizeof(char) * (MAX_LEN_WORD + 1));

    for (fc.num_lines = 0; fscanf(fp, "%s\n", tmp) != EOF; fc.num_lines++)
    {
        if (fc.num_lines == max_lines) {
            max_lines *= 2;
            fc.lines = realloc(fc.lines, sizeof(char*) * max_lines);
            if (fc.lines == NULL) {
                printf("Cannot assign enough memory to store all words");
                exit(1);
            }
        }
        
        fc.lines[fc.num_lines] = malloc(sizeof(char) * (strlen(tmp) + 1));
        strcpy(fc.lines[fc.num_lines], tmp);
    }
    
    free(tmp);
    return fc;
}
