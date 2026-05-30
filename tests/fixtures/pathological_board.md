# Inbox

- [ ] Normal task #AI [score::15]
- [x] Completed task [due::2026-06-01]
- [/] In progress task #Python #Backend
- [>] Delegated task [time::2h]
- [-] Cancelled task

This is just random text and should be ignored.

* Bullet without checkbox
1. Ordered list item

---

# Empty Section



# Weird Spacing

 - [ ] Leading space task
- [ ]    Multiple spaces before title
- [ ] Task with trailing spaces    
- [ ]    Mixed    spacing    inside

# Broken Metadata

- [ ] Missing closing bracket [score::15
- [ ] Missing opening bracket score::15]
- [ ] Empty metadata []
- [ ] Invalid score [score::abc]
- [ ] Invalid due date [due::tomorrow]
- [ ] Broken separator [score=15]
- [ ] Double metadata [score::10] [due::2026-01-01]

# Unicode

- [ ] Русская задача #Проект
- [ ] 日本語タスク #仕事
- [ ] Emoji task 🚀 #Launch
- [ ] Mixed unicode задача 日本語 🚀

# Duplicate Tags

- [ ] Duplicate tags #AI #AI #AI
- [ ] Similar tags #ai #AI #Ai

# Strange Headers

###
#####
#     
# [Broken Header]
# TODO:::
## Waiting???
# ARCHIVE [WIP::10]

# Weird Task Syntax

-[ ] Missing space after dash
-[] Missing spaces in checkbox
- [x Missing closing bracket
- x] Missing opening bracket
- [??] Unknown status
- [/]Valid without space
- [ ]Valid task after malformed ones

# Date Edge Cases

- [ ] Leap year valid [due::2028-02-29]
- [ ] Invalid leap year [due::2027-02-29]
- [ ] Impossible month [due::2026-13-01]
- [ ] Impossible day [due::2026-12-99]

# Metadata Edge Cases

- [ ] Nested metadata [meta::[value]]
- [ ] Colon explosion [a::b::c::d]
- [ ] Empty value [score::]
- [ ] Empty key [::15]
- [ ] Huge score [score::999999999]
- [ ] Negative score [score::-15]

# Multitag Chaos

- [ ] TagsEverywhere #AI#Python#ML
- [ ] Tag punctuation #AI,#ML,#Ops
- [ ] Tag with unicode #Проект #仕事

# Weird Task Syntax

* [ ] Unsupported star marker
+ [ ] Unsupported plus marker
-[] Missing space
- [ ]Valid without space

# Archive

- [x] Archived completed task
- [-] Archived cancelled task


# Noise

```python
def broken():
    return "parser should ignore this"
````

| Table | Row |
| ----- | --- |
| data  | 42  |

> Blockquote task imitation
>
> * [ ] Fake nested task

<!-- HTML Comment -->

<script>
alert("not today")
</script>

# Final

- [ ] Last valid task #Final [score::5]