/* Vākya Native Runtime — Collections (Suchi & Naksha) */
#ifndef VAKYA_COLLECTIONS_H
#define VAKYA_COLLECTIONS_H

#include <stdint.h>
#include <stdbool.h>
#include "memory.h"
#include "panic.h"

/* Dynamic Array (Suchi) */
typedef struct {
    int64_t* items;
    size_t length;
    size_t capacity;
} VakyaList;

static inline VakyaList* vakya_list_new(size_t initial_cap) {
    VakyaList* list = (VakyaList*)vakya_alloc(sizeof(VakyaList));
    list->length = 0;
    list->capacity = initial_cap > 4 ? initial_cap : 4;
    list->items = (int64_t*)vakya_alloc(list->capacity * sizeof(int64_t));
    return list;
}

static inline void vakya_list_push(VakyaList* list, int64_t val) {
    if (list->length >= list->capacity) {
        list->capacity *= 2;
        list->items = (int64_t*)vakya_realloc(list->items, list->capacity * sizeof(int64_t));
    }
    list->items[list->length++] = val;
}

static inline int64_t vakya_list_get(const VakyaList* list, int64_t index) {
    if (index < 0 || (size_t)index >= list->length) {
        vakya_panic("E302", "List index out of bounds in native execution");
    }
    return list->items[index];
}

static inline void vakya_list_set(VakyaList* list, int64_t index, int64_t val) {
    if (index < 0 || (size_t)index >= list->length) {
        vakya_panic("E302", "List index out of bounds in native assignment");
    }
    list->items[index] = val;
}

static inline void vakya_list_free(VakyaList* list) {
    if (list) {
        vakya_free(list->items);
        vakya_free(list);
    }
}

#endif /* VAKYA_COLLECTIONS_H */
