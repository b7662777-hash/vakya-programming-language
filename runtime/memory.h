/* Vākya Native Runtime — Memory & Allocations */
#ifndef VAKYA_MEMORY_H
#define VAKYA_MEMORY_H

#include <stdlib.h>
#include <stdint.h>
#include "panic.h"

static inline void* vakya_alloc(size_t bytes) {
    void* ptr = malloc(bytes);
    if (!ptr && bytes > 0) {
        vakya_panic("E304", "Out of memory in native allocator");
    }
    return ptr;
}

static inline void* vakya_realloc(void* ptr, size_t new_bytes) {
    void* new_ptr = realloc(ptr, new_bytes);
    if (!new_ptr && new_bytes > 0) {
        vakya_panic("E304", "Out of memory in native reallocator");
    }
    return new_ptr;
}

static inline void vakya_free(void* ptr) {
    if (ptr) {
        free(ptr);
    }
}

#endif /* VAKYA_MEMORY_H */
