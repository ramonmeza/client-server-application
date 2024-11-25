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

#### 0x00 echo

| offset | type   | description           |
| ------ | ------ | --------------------- |
| 0      | uint16 | length of text (n)    |
| 2      | bytes  | n bytes of ascii text |

#### 0x01- 0xFF

Reserved for future messages
