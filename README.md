# Client/Server Application

My attempt at creating some client/server interactions utilizing TCP and designing
custom protocols to interact with the server.

## Running the Application

If you are utilizing `pdm`, simply run the command

```sh
# run the server with specified parameters
pdm run server --host "127.0.0.1" --port 5000
pdm run client
```

### Server

- listens for incoming connections
- parses received data based on protocol specificiation
- handles message routing to services based on received message

### Client

- a client-side shell to interact with the server

## Protocol Designs

| offset | type   | description                        |
| ------ | ------ | ---------------------------------- |
| 0      | uint8  | the id for this type of message    |
| 1      | uint32 | the amount of bytes in the message |
| 5      | ...    | the message data                   |

### Message Types

#### Miscelaneous

##### 0x00 echo

Echo a message.

| offset | type   | description           |
| ------ | ------ | --------------------- |
| 0      | uint16 | length of text (n)    |
| 2      | bytes  | n bytes of ascii text |

#### Chat Room

##### 0x01 request id

Request to join a chatroom with your given username.

| offset | type  | description               |
| ------ | ----- | ------------------------- |
| 0      | uint8 | length of username (n)    |
| 1      | bytes | n bytes of ascii username |

##### 0x02 request id response

Response message to request id that contains the unique id (UUID) that is linked to the user and the room ID they have connected to.

| offset | type   | description               |
| ------ | ------ | ------------------------- |
| 0      | uint32 | uuid linked to a username |
| 4      | uint32 | room id                   |

##### 0x03 send message

Send messages to the chatroom.

| offset | type   | description               |
| ------ | ------ | ------------------------- |
| 0      | uint32 | uuid linked to a username |
| 4      | uint32 | room id                   |
| 8      | uint16 | length of text (n)        |
| 10     | bytes  | n bytes of ascii text     |

##### 0x04 receive message

Messages sent by the server. Receives messages and their corresponding sender's username.

| offset     | type   | description               |
| ---------- | ------ | ------------------------- |
| 0          | uint32 | uuid linked to a username |
| 4          | uint32 | room id                   |
| 8          | uint8  | length of username (n)    |
| 9          | bytes  | n bytes of ascii username |
| 9 + n      | uint16 | length of text (m)        |
| 11 + n + m | bytes  | n bytes of ascii text     |

##### 0x05 leave chat room

Leave the chatroom.

| offset | type   | description               |
| ------ | ------ | ------------------------- |
| 0      | uint32 | uuid linked to a username |
| 4      | uint32 | room id                   |

#### 0x06-0xFF

Reserved for future messages
