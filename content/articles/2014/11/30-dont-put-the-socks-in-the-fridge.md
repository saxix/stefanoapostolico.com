Title: Don't put the socks in the fridge
status: published
category: it

In response to a set of recommendations I was presenting about an Enterprise 
Java solution architecture, a CTO once asked me: 
*"Yeah, we've got this 2 GB EAR with 400+ WAR deployments inside. 
So what's the problem? The system still is completely functional!"*. 
My instant feeling was 
*"Ok, this CTO himself is a much bigger problem than this EAR!"*

<!-- PELICAN_END_SUMMARY -->

A few years ago, I was in India to train developers of a local IT company. 
It was a great experience - I met a lot of wonderful people there, few of whom 
I'm still in touch with. Many of them were good developers, working hard with a hunger 
to learn their subjects deeply at work. Much of the focus in my sessions was on practices 
of designing large scale object-oriented systems. In a conversation about core design 
principles, during a rapid fire response, I submitted to them this idea - 
*"Yes, you can put the socks in the fridge, but choose NOT to put it there!"*. 

My intent was to explain that when you design there is a place for everything, and sometimes a written rule or law is not needed to feel that something is wrongly placed (beyond principles of High Cohesion and Least Surprise, there is common sense, fundamental cleanliness to respect). The metaphor resonated with them instantly - they immediately understood the principle without any further debate. 

At that time I had no idea how many times I would have to use it again and again!

In further years, I found it very frustrating when people claiming to be technical leads and architects taking the stand of "it isn't wrong if there's no rule that says so", like "no rule says you can't mix SQL with HTML markup" or "no rule says you can't use spaces for the dictionary keys for a REST API". Much effort to make them see beyond the need of defining rules for everything - with long explanations about the innumerable risks in such design - were mostly futile. They'd rather stick to approved rules than take a lead or leap of faith in common sense.

When you find yourself submitting an idea or approach widely shared by the community as a convention (with profound logic behind it that you know and understand), only to be countered by your audience saying "Show me the rule defining so" - take a hint and end the discussion as soon as possible. I've come to understand that such resistance doesn't come from the unfamiliarity of the topic - but from the gap between the interlocutors from a technical standpoint and more seriously, the values standpoint. 

It's not about fighting, but it's about choosing your fights!
