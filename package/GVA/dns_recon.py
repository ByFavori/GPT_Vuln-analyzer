from typing import Any
from typing import Optional

import dns.resolver
import openai
from rich.progress import track

model_engine = "text-davinci-003"


def AI(key: str, data: Any) -> str:
    openai.api_key = key
    try:
        prompt = "do a DNS analysis of {} and return proper clues for an attack in json".format(
            data)
        # A structure for the request
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
        )
        response = completion.choices[0].text
        return str(response)
    except KeyboardInterrupt:
        print("Bye")
        quit()


def dns_recon(target: Optional[str], key: str) -> str:
    if key is not None:
        pass
    else:
        raise ValueError("KeyNotFound: Key Not Provided")
    if target is not None:
        pass
    else:
        raise ValueError("InvalidTarget: Target Not Provided")
    analyze = ''
    # The DNS Records to be enumeratee
    record_types = ['A', 'AAAA', 'NS', 'CNAME', 'MX', 'PTR', 'SOA', 'TXT']
    for records in track(record_types):
        try:
            answer = dns.resolver.resolve(target, records)
            for server in answer:
                st = server.to_text()
                analyze += "\n"
                analyze += records
                analyze += " : "
                analyze += st
        except dns.resolver.NoAnswer:
            print('No record Found')
            pass
        except dns.resolver.NXDOMAIN:
            print('NXDOMAIN record NOT Found')
            pass
        except KeyboardInterrupt:
            print("Bye")
            quit()
    try:
        response = AI(key, analyze)
        return str(response)
    except KeyboardInterrupt:
        print("Bye")
        quit()
