#ifndef PROTOCOL_H
#define PROTOCOL_H

/*
 * ==========================================================
 * Communication Protocol
 * ==========================================================
 *
 * Handles JSON communication between the ESP32 and
 * the desktop application.
 */

void initializeProtocol();

void processIncomingCommands();

#endif