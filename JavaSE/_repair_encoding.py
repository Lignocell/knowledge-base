# -*- coding: utf-8 -*-
"""
修复 集合类.md 的编码损坏。
损坏模式：UTF-8 文本被按 GBK 解码后又以 UTF-8 存回（典型“濡傛灉”型乱码）。
逆转方法：乱码文本 .encode('gbk') -> .decode('utf-8')。
注意：当初 GBK 解码失败的字节已变成 '?'，这些字节不可逆，修复后会留下 � 标记，需人工对照补全。
"""
import re

SRC = '集合类.md'
DST = '集合类.repaired.md'
REPORT = '_repair_report.txt'

def bad_score(s: str) -> int:
    """乱码嫌疑分：替换符 + 私有区字符 + 高频乱码汉字区间"""
    score = s.count('�')
    score += sum(1 for c in s if 0xE000 <= ord(c) <= 0xF8FF)          # PUA
    score += len(re.findall(r'[鍙-鏋锟-闄濡-艑纟-鹫]', s))        # 典型GBK逆转UTF8乱码字
    return score

raw = open(SRC, 'rb').read()
text = raw.decode('utf-8-sig')
lines = text.split('\n')

fixed_lines = []
report = []
n_fixed = n_kept = 0
for i, ln in enumerate(lines, 1):
    orig_bad = bad_score(ln)
    if orig_bad == 0:
        fixed_lines.append(ln)
        n_kept += 1
        continue
    try:
        candidate = ln.encode('gbk', errors='replace').decode('utf-8', errors='replace')
    except Exception as e:
        fixed_lines.append(ln)
        report.append(f'line {i}: encode/decode failed: {e}')
        n_kept += 1
        continue
    cand_bad = bad_score(candidate)
    if cand_bad < orig_bad:
        fixed_lines.append(candidate)
        n_fixed += 1
        lost = candidate.count('�')
        if lost:
            report.append(f'line {i}: FIXED but {lost} byte(s) unrecoverable: {candidate.strip()[:80]}')
    else:
        fixed_lines.append(ln)
        report.append(f'line {i}: reversal NOT better (orig {orig_bad} vs cand {cand_bad}), kept original: {ln.strip()[:80]}')
        n_kept += 1

result = '\n'.join(fixed_lines)
with open(DST, 'w', encoding='utf-8-sig', newline='') as f:
    f.write(result)

total_fffd = result.count('�')
summary = [
    f'lines total: {len(lines)}',
    f'lines reversed: {n_fixed}',
    f'lines kept as-is: {n_kept}',
    f'remaining unrecoverable markers (�): {total_fffd}',
    '',
    '=== details ===',
] + report
with open(REPORT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(summary))
print('\n'.join(summary[:6]))
