/* Vākya Native Runtime — Panic & Error Handling */
#ifndef VAKYA_PANIC_H
#define VAKYA_PANIC_H

#include <stdio.h>
#include <stdlib.h>

static inline void vakya_panic(const char* error_code, const char* message) {
    fprintf(stderr, "\n\033[1;31mError [%s]: %s\033[0m\n\n", error_code, message);
    exit(1);
}

#endif /* VAKYA_PANIC_H */
