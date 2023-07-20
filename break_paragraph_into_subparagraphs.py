def break_paragraph_into_subparagraphs(paragraph, max_length=2000):
    sub_paragraphs = []
    while len(paragraph) > max_length:
        # Find the last period within the maximum length
        last_period_index = paragraph.rfind(".", 0, max_length)
        if last_period_index == -1:
            # If no period is found within the maximum length, just split at the max length
            sub_paragraph = paragraph[:max_length]
            paragraph = paragraph[max_length:]
        else:
            # Split at the last period found
            sub_paragraph = paragraph[:last_period_index + 1]
            paragraph = paragraph[last_period_index + 1:]
        sub_paragraphs.append(sub_paragraph)

    # Append the remaining part of the paragraph, which is now less than the max_length
    if paragraph:
        sub_paragraphs.append(paragraph)

    return sub_paragraphs

# Example usage:
original_paragraph = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla id nisi sit amet risus luctus ullamcorper. Suspendisse potenti. Etiam eleifend, mi ac scelerisque hendrerit, tortor mi facilisis sapien, vel volutpat felis sapien eu elit. Fusce euismod in mi id dapibus. Curabitur nec mi eleifend, feugiat quam a, vestibulum justo. Sed tincidunt id tellus eget mollis. Integer sit amet quam eu justo facilisis tincidunt. Phasellus ac tincidunt tellus. Nullam rhoncus dictum nibh, ac ultricies est feugiat a. Nullam ac fermentum sapien, sit amet cursus felis. Aenean gravida in metus ac egestas. Proin sed neque a sem congue cursus vel in ligula. Vivamus cursus tortor a dui commodo, sit amet hendrerit nisi bibendum. Quisque eu quam vel elit luctus volutpat a nec ex. Vestibulum ut ipsum id odio congue ultrices. Morbi vehicula eros at elit congue venenatis. Vestibulum efficitur turpis vitae ipsum aliquam, nec bibendum turpis iaculis. Aenean vulputate odio in quam malesuada, a aliquet ligula semper. Integer ullamcorper orci sed eleifend volutpat. Sed vel felis odio. Etiam bibendum malesuada nulla sit amet facilisis. In vitae justo ac tellus facilisis mattis non ac elit.

Donec feugiat augue in justo lacinia, sit amet bibendum elit feugiat. Proin euismod metus eu nulla aliquet, in sagittis risus efficitur. In vestibulum, mauris ac convallis suscipit, eros urna laoreet libero, id iaculis urna nisl vitae tellus. Nullam tincidunt nisi non varius efficitur. Mauris ultricies ipsum ut diam tempus, eu sagittis orci ultricies. Suspendisse rhoncus ex a ex efficitur, vel aliquam elit bibendum. Nulla facilisi. Integer ultrices mauris eu ipsum euismod pellentesque. Nunc eleifend odio in gravida commodo. Sed eget efficitur ipsum. Ut sit amet mi vel magna rhoncus malesuada nec ut velit. Vivamus dictum ullamcorper dui, eget blandit ex rhoncus a. Nulla facilisi.

Sed dictum odio et est mattis malesuada. Sed vel lectus in turpis dignissim sodales. Fusce sit amet varius elit. Aenean aliquam mi sapien, et pellentesque ex lacinia at. Vestibulum a faucibus justo. Nunc auctor felis eu turpis interdum, nec pharetra erat consequat. Nam aliquam, arcu nec rhoncus mattis, nunc dui congue purus, eu venenatis erat odio nec ante. Sed ut eleifend lorem, at malesuada odio. Aenean eu ante ipsum. Fusce vel facilisis eros. Vestibulum eget ex quis enim vulputate dapibus ac id ex. Donec volutpat euismod enim in egestas.

Nunc facilisis ultrices ante, a eleifend turpis hendrerit et. Praesent ac velit quis velit egestas vulputate. Nam elementum tellus sit amet justo mollis, non consectetur felis dictum. Aliquam eget justo et libero fermentum rutrum. Sed vel enim in sapien scelerisque consectetur. Nullam bibendum feugiat massa, eu vehicula odio. Fusce vestibulum ligula ut massa cursus, ac finibus velit suscipit. Curabitur vel interdum quam. Sed ultrices hendrerit turpis. Integer euismod risus in arcu dignissim, nec venenatis purus rhoncus. Vestibulum dignissim urna eu mauris bibendum rhoncus. Nulla nec dolor ut nulla tristique cursus. Vestibulum eget convallis quam.

Nam vel nisi vel urna posuere bibendum a nec augue. Nunc aliquam eu mauris ut vestibulum. Duis mattis consectetur ex a pharetra. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed convallis, urna vitae mattis tempus, metus tellus bibendum dui, vel facilisis nisl mi sit amet urna. Suspendisse eu feugiat quam, nec bibendum dolor. Proin pulvinar risus eget mauris mattis congue. Duis hendrerit, metus sit amet laoreet rutrum, turpis mi interdum ex, vitae bibendum sapien purus ut urna. Aenean dictum lacus euismod risus fermentum bibendum. In auctor, massa vel feugiat rhoncus, erat dui hendrerit neque, vel vehicula erat odio sit amet felis. Sed volutpat ullamcorper nisl, eu sagittis sem venenatis at. Fusce interdum massa id ex aliquam elementum.

Donec nec nisl rhoncus, finibus orci eu, suscipit magna. Proin tempus gravida volutpat. Nulla facilisi. Vestibulum eu purus in nunc finibus accumsan. Nunc vehicula est vel sapien pharetra, at tempor ligula ultrices. In id magna id turpis ullamcorper eleifend non vitae nulla
"""

sub_paragraphs = break_paragraph_into_subparagraphs(original_paragraph)
print(len(sub_paragraphs))
print(sub_paragraphs)