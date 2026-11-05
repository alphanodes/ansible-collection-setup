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

The rules live in the tables `inet netfilter` and `ip netfilter-nat`, which the configuration replaces atomically on every reload. The table `inet f2b-table` of fail2ban and the tables `ip filter` and `ip nat` of iptables-nft (used by Docker) are not touched, so bans survive a reload. The states `disabled` and `remove` only delete the tables of this role and do not stop `nftables.service`, because stopping it flushes the whole ruleset including the bans.

## Migration from iptables

Hosts set up with the former iptables engine of this role still carry the rules of iptables-persistent in the kernel. Once the nftables rules are active, the role flushes them and removes iptables-persistent. The `iptables` package itself stays installed if it was. Compared to the iptables rules the output allowlist now matches the destination (`netfilter_allowed_networks_output`), honeypot hits are tracked in a dynamic set with timeout instead of the xt_recent module.
