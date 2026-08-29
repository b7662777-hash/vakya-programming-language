/* Vākya Native Runtime — String Operations */
#ifndef VAKYA_STRINGS_H
#define VAKYA_STRINGS_H

#include <string.h>
#include <stdio.h>
#include "memory.h"

typedef struct {
    char* data;
    size_t length;
} VakyaString;

static inline VakyaString* vakya_string_new(const char* cstr) {
    VakyaString* s = (VakyaString*)vakya_alloc(sizeof(VakyaString));
    s->length = cstr ? strlen(cstr) : 0;
    s->data = (char*)vakya_alloc(s->length + 1);
    if (cstr) {
        memcpy(s->data, cstr, s->length);
    }
    s->data[s->length] = '\0';
    return s;
}

static inline VakyaString* vakya_string_concat(const VakyaString* a, const VakyaString* b) {
    size_t len_a = a ? a->length : 0;
    size_t len_b = b ? b->length : 0;
    VakyaString* res = (VakyaString*)vakya_alloc(sizeof(VakyaString));
    res->length = len_a + len_b;
    res->data = (char*)vakya_alloc(res->length + 1);
    if (a && a->data) {
        memcpy(res->data, a->data, len_a);
    }
    if (b && b->data) {
        memcpy(res->data + len_a, b->data, len_b);
    }
    res->data[res->length] = '\0';
    return res;
}

static inline void vakya_string_free(VakyaString* s) {
    if (s) {
        vakya_free(s->data);
        vakya_free(s);
    }
}

#endif /* VAKYA_STRINGS_H */
