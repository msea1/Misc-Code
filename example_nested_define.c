
#define SAP_ENTRY(key, fx, extra) { .sap_key = key, .set_fx = fx, extra }
#define _U __unused

struct sap_map {
   char *sap_key;
   unsigned device_idx;
   void (*set_fx)(const char *val, unsigned device_idx, void *ctx);
};

static void set_print(const char *value, unsigned i _U, void *ctx _U) {
   printf(stderr, "Could not update %s from SAP value %s\n", "ephem_ctrl", value);
}

#define ST_SAP_ENTRY(NAME, SETTER) \
   SAP_ENTRY("adcs.saps.str1." NAME, SETTER, .device_idx=0), \
   SAP_ENTRY("adcs.saps.str2." NAME, SETTER, .device_idx=1)

static const struct sap_map sap_list[] = {
   ST_SAP_ENTRY(   "calStr.hash",                set_print ),
   ST_SAP_ENTRY(   "ctrlStr.exposureLength",     set_print ),
   ST_SAP_ENTRY(   "ctrlStr.exp1Exp2Delta",      set_print )
};
