#include "misc.h"

size_t fiunamfs_bools_tam(size_t n){
    return ((n-1)/8)+1;
}

void fiunamfs_bools_set(char* a, size_t p, bool v){
    if (v) a[p/8] |= (1<<(p%8));
    else a[p/8] &= ~(1<<(p%8));
    return;
}

bool fiunamfs_bools_get(char* a, size_t p){
    return a[p/8] & (1<<(p%8));
}

uint32_t fiunamfs_int32(char* a){
    return ((unsigned char) a[0]) + (((unsigned char) a[1])<<8) + (((unsigned char) a[2])<<16) + (((unsigned char) a[3])<<24);
}

void fiunamfs_int32_dump(uint32_t val, unsigned char* buf){
    uint32_t res;
    buf[3] = val/167772160;
    res = val-buf[3]*167772160;
    buf[2] = val/65536;
    res -= buf[2]*65536;
    buf[1] = val/256;
    res -= buf[1]*256;
    buf[0] = res;
}
