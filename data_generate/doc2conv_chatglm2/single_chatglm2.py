import os
import sys
os.environ['CUDA_VISIBLE_DEVICES']='0'

from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("D:/LLM-code/LLM_Models/chatglm2-6b-int4/", trust_remote_code=True)
model = AutoModel.from_pretrained("D:/LLM-code/LLM_Models/chatglm2-6b-int4/", trust_remote_code=True, device='cuda')
model = model.eval()


in_file = sys.argv[1]
out_file = sys.argv[2]

# prompt = '请根据文档生成一段对话。\n\n文档1:\n当网红、做直播，正成为不少年轻人期待的工作。微博近日发布一项“当代年轻人就业在关注什么”问卷数据：近万名受访应届毕业生中，61.6%的人就业时会考虑网红直播等新兴职业，只有38.4%选择完全不考虑。另有数据显示，2022年，直播、短视频行业直接或间接带动的就业机会超1亿个。越来越多年轻人“打开思路”，试图加入直播等新兴行业。但这行真的那么“好赚”吗？“网红”是不是个有前途的职业选择？大量应届毕业生加入直播行业据国是直通车，对于上述微博问卷数据，有12年就业辅导经验的职业发展经纪人佟志刚表示，该数据相对真实地反映了当前毕业生的求职预期变化。从他接触的求职者来看，2022年开始，越来越多应届毕业生希望能兼职做主播。'\
#     '\n\n生成的对话1:\nA: 最近微博发布了一份关于年轻人就业关注点的问卷数据，显示有近万名受访的应届毕业生中，61.6%的人在就业时会考虑网红直播等新兴职业，而只有38.4%的人选择完全不考虑。这意味着越来越多的年轻人希望从事直播等新兴行业了。\nB: 是啊，我也听说了。我觉得这可能是因为直播、短视频行业在2022年带动的就业机会超过了1亿个，所以年轻人开始对这个行业产生了兴趣。\nA: 但是我一直在想，网红这个职业真的那么好赚吗？毕竟现在市场上已经有很多网红了，竞争应该很激烈吧。\n\n文档2:\n{}\n\n生成的对话2:'

prompt = '文档:\n{}'

his = [
    ('请根据文档生成一段两人对话，用A表示第一个人，B表示第二个人，对话以A开始，以B结束。\n\n文档:\n当网红、做直播，正成为不少年轻人期待的工作。微博近日发布一项“当代年轻人就业在关注什么”问卷数据：近万名受访应届毕业生中，61.6%的人就业时会考虑网红直播等新兴职业，只有38.4%选择完全不考虑。另有数据显示，2022年，直播、短视频行业直接或间接带动的就业机会超1亿个。越来越多年轻人“打开思路”，试图加入直播等新兴行业。但这行真的那么“好赚”吗？“网红”是不是个有前途的职业选择？大量应届毕业生加入直播行业据国是直通车，对于上述微博问卷数据，有12年就业辅导经验的职业发展经纪人佟志刚表示，该数据相对真实地反映了当前毕业生的求职预期变化。从他接触的求职者来看，2022年开始，越来越多应届毕业生希望能兼职做主播。',
    'A: 最近微博发布了一份关于年轻人就业关注点的问卷数据，显示有近万名受访的应届毕业生中，61.6%的人在就业时会考虑网红直播等新兴职业，而只有38.4%的人选择完全不考虑。这意味着越来越多的年轻人希望从事直播等新兴行业了。\nB: 是啊，我也听说了。我觉得这可能是因为直播、短视频行业在2022年带动的就业机会超过了1亿个，所以年轻人开始对这个行业产生了兴趣。\nA: 但是我一直在想，网红这个职业真的那么好赚吗？毕竟现在市场上已经有很多网红了，竞争应该很激烈吧。\nB: 对，竞争确实很激烈。我听说很多应届毕业生都想兼职做主播，但是不知道他们真的能在这个行业立足吗？')
    ]

with open(in_file, 'r', encoding='utf-8') as fin,\
    open(out_file, 'w', encoding='utf-8') as fout:
    doc = fin.read()
    input = prompt.format(doc)

    print(input)
    response, history = model.chat(tokenizer, input, history=his)
    print(response)
    fout.write(response)


response, history = model.chat(tokenizer, "晚上睡不着应该怎么办", history=history)
print(response)


# python single_chatglm2.py example.txt example_conv.txt