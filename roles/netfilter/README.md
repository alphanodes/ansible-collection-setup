# Ansible Role: netfilter

Host firewall with nftables for Debian and Ubuntu servers: incoming traffic is dropped except for the configured ports, sources and the SSH port, with an optional honeypot for port scanners and NAT rules.

## Role Variables

Available variables can be found in [defaults/main.yml](defaults/main.yml)

## Example Playbook

```yaml
    - hosts: all

      vars:
        netfilter_state: active
        netfilter_allowed_tcp_ports:
          - 80
          - 443
        netfilter_ssh_sources:
          - 192.0.2.0/24

      roles:
        - alphanodes.setup.netfilter
```

## Integration with fail2ban

The rules live in the tables `inet netfilter` and `ip netfilter-nat`, which the configuration replaces atomically on every reload. The table `inet f2b-table` of fail2ban and the tables `ip filter` and `ip nat` of iptables-nft (used by Docker) are not touched, so bans survive a reload. The states `disabled` and `remove` only delete the tables of this role, empty the configuration file and stop the service, so the rules do not come back with a package upgrade. A drop-in removes the `ExecStop` of `nftables.service`, which would flush the whole ruleset including the bans on every stop and on the restart Debian performs when the package is upgraded.

## Rule Order

Trusted sources, ssh and zabbix are accepted first, so a honeypot hit never locks them out. Then known scanners are dropped, then the public ports are accepted, and only then the honeypot traps follow, so a port opened in `netfilter_allowed_tcp_ports` is never a trap. Behind NAT a single infected client would lock out everybody sharing the address on the public ports, set the honeypot lists empty there.

## Outgoing Connections

The output chain rejects connections of `netfilter_metadata_blocked_users` to the cloud metadata service and connections to port 25 of other hosts by anyone but `netfilter_output_smtp_users`. Applications have to deliver through the local mail server. Only users existing at the time of the run are used, as nft refuses a configuration with unknown users, so a user created by a later role is added with the next run.

## Migration from iptables

Hosts set up with the former iptables engine of this role still carry the rules of iptables-persistent in the kernel. Once the nftables rules are active (state `active` only), the role flushes them, removes iptables-persistent and deletes the then empty tables of iptables-nft (`ip filter`, `ip nat`, ...). Rules added manually with `netfilter-persistent save` are lost at that point, compare `iptables-save` with the host variables before the first run. The `iptables` package itself stays installed if it was. Compared to the iptables rules the output allowlist now matches the destination (`netfilter_allowed_networks_output`), honeypot hits are tracked in a dynamic set with timeout instead of the xt_recent module.
