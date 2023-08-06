# richify

Automatically rich highlight arbitrary text output in your terminal.

## Dependencies

 - [Python 3.x](https://python.org)
 - [Textualize/rich](https://github.com/Textualize/rich)

## Installation

```sh
$  pip install richify
```

## Usage Examples

```sh
$  dmesg | richify
```

```sh
$  apt show git | richify
```

```sh
ifconfig | richify
```

```sh
journalctl -ru ssh | richify --color=always | less -R
```