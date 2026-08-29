/* Vākya Native Runtime — I/O and Standard Output */
#ifndef VAKYA_IO_H
#define VAKYA_IO_H

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include "strings.h"
#include "collections.h"

static inline void vakya_vada_int(int64_t x) {
    printf("%lld\n", (long long)x);
}

static inline void vakya_vada_float(double x) {
    printf("%g\n", x);
}

static inline void vakya_vada_str(const VakyaString* s) {
    if (s && s->data) {
        printf("%s\n", s->data);
    } else {
        printf("shunya\n");
    }
}

static inline void vakya_vada_cstr(const char* s) {
    printf("%s\n", s ? s : "shunya");
}

static inline void vakya_vada_bool(bool b) {
    printf("%s\n", b ? "satya" : "asatya");
}

static inline void vakya_vada_list(const VakyaList* list) {
    if (!list) {
        printf("[]\n");
        return;
    }
    printf("[");
    for (size_t i = 0; i < list->length; ++i) {
        if (i > 0) printf(", ");
        printf("%lld", (long long)list->items[i]);
    }
    printf("]\n");
}

#endif /* VAKYA_IO_H */
