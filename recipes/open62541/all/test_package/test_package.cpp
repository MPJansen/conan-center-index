/* This work is licensed under a Creative Commons CCZero 1.0 Universal License.
 * See http://creativecommons.org/publicdomain/zero/1.0/ for more information. */

#include <open62541/client_config_default.h>
#include <open62541/client_highlevel.h>
#include <open62541/client_subscriptions.h>
#include <open62541/plugin/log_stdout.h>

#include <stdlib.h>
int main(int argc, char *argv[]) {
    UA_Client *client = UA_Client_new();
    UA_ClientConfig_setDefault(UA_Client_getConfig(client));
    UA_ClientState state = UA_Client_getState(client);
    switch (state)
    {
    case UA_CLIENTSTATE_DISCONNECTED: printf("disconnected\n"); break;
    case UA_CLIENTSTATE_CONNECTED: printf("connected\n"); break;
    case UA_CLIENTSTATE_SECURECHANNEL: printf("secure channel\n"); break;
    case UA_CLIENTSTATE_SESSION: printf("session\n"); break;
    case UA_CLIENTSTATE_SESSION_RENEWED: printf("session renewed\n"); break;
    default: break;
    }
    UA_Client_delete(client); /* Disconnects the client internally */
    return 0;
    return EXIT_SUCCESS;
}