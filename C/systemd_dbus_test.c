// see dbus_python_service.py

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <inttypes.h>
#include <systemd/sd-bus.h>
#include <systemd/sd-daemon.h>

#define DS "sand.box"
#define DO "/sand/box"
#define DI "sand.box.cmds"
#define TO 2 * 1000 * 1000

#define X_SAP "a_sap"
#define Y_SAP "b_sap"

/*   SERVICE STUFF    */
struct cached_saps {
    bool x;
    double y;
} g_sap_cache;


struct sap_setters {
    char *sap_key;
    void (*set_fx)(char *val); // pointer to setter fx
} g_saps;

/*   END SERVICE STUFF    */


/*   SFUTILS STUFF    */

void s_to_char(int k, struct sap_setters *sl, char **saps_out) {
    printf("SL.in is [%s, %s] at %p\n", sl[0].sap_key, sl[1].sap_key, &sl);

    for (int i = 0; i < k; i++) {
        if (sl[i].sap_key != NULL) {
            saps_out[i] = strdup(sl[i].sap_key);
        }
    }
    saps_out[k-1] = NULL;
    printf("SL.out is [%s, %s] at %p\n", sl[0].sap_key, sl[1].sap_key, &sl);
    printf("Keys out are [%s, %s, %s] at %p\n", saps_out[0], saps_out[1], saps_out[2], saps_out);
}

void read_as(int num_keys, struct sap_setters *sl, char **values_out)
{
    printf("Keys is %d\n", num_keys);

    char *keys[num_keys];
    s_to_char(num_keys, sl, keys);
    printf("Keys are [%s, %s, %s] at %p\n", keys[0], keys[1], keys[2], keys);

    sd_bus *bus = NULL;
    sd_bus_default(&bus);

    sd_bus_message *msg = NULL;
    int rv = sd_bus_message_new_method_call(bus, &msg, DS, DO, DI, "Ack");
    rv = sd_bus_message_append_strv(msg, keys);

    sd_bus_error error = {};
    sd_bus_message *reply = NULL;

    rv = sd_bus_call(bus, msg, TO, &error, &reply);

    char **what = NULL;
    rv = sd_bus_message_read_strv(reply, &what);

    printf("Reply is [%s, %s] at %p pointing to %p\n", what[0], what[1], &what, what);
    printf("iV.1 is [%s, %s] at %p pointing to %p\n", values_out[0], values_out[1], &values_out, values_out);

    for (int i = 0; i < num_keys; i++) {
        if (what[i] != NULL) {
            values_out[i] = strdup(what[i]);
            free(what[i]);
        }
        else {
            values_out[i] = NULL;
        }
    }
    printf("SL.out3 is [%s, %s] at %p\n", sl[0].sap_key, sl[1].sap_key, &sl);
    printf("iV.2 is [%s, %s] at %p pointing to %p\n", values_out[0], values_out[1], &values_out, values_out);
    free(what);
    printf("iV.3 is [%s, %s] at %p pointing to %p\n", values_out[0], values_out[1], &values_out, values_out);
}

bool get_value(char *sap_key, int k, char **kv_msg, char **value_out)
{
    char *sap = NULL;
    for (int i = 0; i < k; i++) {
        printf("Looking for %s in %s\n", sap_key, kv_msg[i]);
        if (kv_msg[i] == NULL)
            continue;
        sap = strdup(kv_msg[i]);
        char *sap_v = strchr(sap, ':');
        if (sap_v == NULL)
            continue;
        *sap_v++ = '\0';
        if (strcmp(sap, sap_key) == 0) {
            *value_out = strdup(sap_v);
            free(sap);
            return true;
        }
    }
    free(sap);
    return false;
}

void parse_as(int k, struct sap_setters *sl, char **kv_msg) {
    char *temp = NULL;
    for (int i = 0; i < k; i++) {
        temp = NULL;
        if (sl[i].sap_key != NULL) {
            if (get_value(sl[i].sap_key, k, kv_msg, &temp) == true){
                sl[i].set_fx(temp);
            }
        }
    }
    free(temp);
}

/*   END SFUTILS STUFF    */

/*     SERVICE STUFF     */

void set_x(char *val) { 
    printf("setting x to %s\n", val);
    unsigned char sv_num = !!(atoi(val)); // normalize to 0 or 1
    g_sap_cache.x = sv_num;
    printf("SAP %s = %s\n", X_SAP, sv_num ? "true" : "false");
}

void set_y(char *val) {
    printf("setting y to %s\n", val);
    double sv;
    if (sscanf(val, "%lf", &sv) == 1) {
        g_sap_cache.y = sv;
        printf("SAP %s = %lf\n", Y_SAP, sv);
    }
    else
        printf("Could not update %s from SAP value %s\n", Y_SAP, val); 
}


int main()
{
    struct sap_setters sap_list[] = {
        { .sap_key = X_SAP, .set_fx = set_x, },
        { .sap_key = Y_SAP, .set_fx = set_y, },
        NULL
    };

    int k_len = sizeof(sap_list)/sizeof(sap_list[0]);

    printf("S.1 has len %d is [%s, %s] at %p\n", k_len, sap_list[0].sap_key, sap_list[1].sap_key, &sap_list);

    char *values[k_len];

    printf("V.1 is %s at %p pointing to %p\n", *values, &values, values);

    read_as(k_len, sap_list, values);

    printf("S.2 is [%s, %s] at %p\n", sap_list[0].sap_key, sap_list[1].sap_key, &sap_list);
    printf("V.2 is [%s, %s] at %p pointing to %p\n", values[0], values[1], &values, values);

    printf("cached.1 is %d, %f\n", g_sap_cache.x, g_sap_cache.y);
    parse_as(k_len, sap_list, values);
    printf("cached.2 is %d, %f\n", g_sap_cache.x, g_sap_cache.y);

    return false;
}