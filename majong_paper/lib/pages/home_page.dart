import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../widgets/wood_background.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _selectedIndex = 0;

  static const List<Widget> _widgetOptions = <Widget>[
    SimpleRecordSheet(), // ← 対局ページ：4列・大型入力ドック付き
    Center(child: Text('履歴ページ')),
    Center(child: Text('設定ページ')),
  ];

  void _onItemTapped(int index) => setState(() => _selectedIndex = index);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('麻雀記録'),
        backgroundColor: Colors.black.withOpacity(0.5),
      ),
      body: WoodBackground(
        child: _widgetOptions.elementAt(_selectedIndex),
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.black.withOpacity(0.5),
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(icon: Icon(Icons.analytics_outlined), label: '対局'),
          BottomNavigationBarItem(icon: Icon(Icons.history), label: '履歴'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: '設定'),
        ],
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
      ),
    );
  }
}

/// ===============================================================
///  シンプル記録表（4列固定 / 1〜8回 / ＋/− / 小計 / 合計）
///  - セルタップで下部に「大型入力ボトムシート（テンキー付き）」
///  - 小計：各列の＋合計 / −合計
///  - 合計：＋ − の差分
/// ===============================================================
class SimpleRecordSheet extends StatefulWidget {
  const SimpleRecordSheet({super.key});
  @override
  State<SimpleRecordSheet> createState() => _SimpleRecordSheetState();
}

class _SimpleRecordSheetState extends State<SimpleRecordSheet> {
  static const int players = 4;
  static const int rounds = 8;

  // 氏名
  late final List<TextEditingController> _nameCtrls =
      List.generate(players, (i) => TextEditingController(text: ['東家','南家','西家','北家'][i]));

  // 本体（＋/−）
  late final List<List<TextEditingController>> _plusCtrls =
      List.generate(players, (_) => List.generate(rounds, (_) => TextEditingController()));
  late final List<List<TextEditingController>> _minusCtrls =
      List.generate(players, (_) => List.generate(rounds, (_) => TextEditingController()));

  bool _autoNext = true; // セット後に次の回へ

  @override
  void dispose() {
    for (final c in _nameCtrls) c.dispose();
    for (final row in _plusCtrls) { for (final c in row) c.dispose(); }
    for (final row in _minusCtrls) { for (final c in row) c.dispose(); }
    super.dispose();
  }

  // ---- helpers ----
  int _toInt(TextEditingController c) {
    final t = c.text.trim();
    if (t.isEmpty) return 0;
    return int.tryParse(t) ?? 0;
  }

  int _sumPlus(int p) => _plusCtrls[p].fold(0, (s, c) => s + _toInt(c));
  int _sumMinus(int p) => _minusCtrls[p].fold(0, (s, c) => s + _toInt(c));
  int _total(int p) => _sumPlus(p) - _sumMinus(p);

  // ---- UI ----
  @override
  Widget build(BuildContext context) {
    const cornerW = 76.0;
    const cellW = 68.0;

    final widths = <int, TableColumnWidth>{
      0: const FixedColumnWidth(cornerW),
      for (int i = 0; i < players * 2; i++) i + 1: const FixedColumnWidth(cellW),
    };

    return ListView(
      padding: const EdgeInsets.all(12),
      children: [
        // 4列の氏名行（回数コーナー付き）
        _paperCard(
          child: Table(
            columnWidths: {
              0: const FixedColumnWidth(cornerW),
              for (int i = 0; i < players; i++) i + 1: const FixedColumnWidth(cellW * 2),
            },
            border: TableBorder.all(color: Colors.black12),
            defaultVerticalAlignment: TableCellVerticalAlignment.middle,
            children: [
              TableRow(
                decoration: const BoxDecoration(color: Color(0xFFF7F7F7)),
                children: [
                  _cellCenter(const Text('回数', style: TextStyle(fontWeight: FontWeight.w600))),
                  for (int p = 0; p < players; p++)
                    Padding(
                      padding: const EdgeInsets.all(6.0),
                      child: TextField(
                        controller: _nameCtrls[p],
                        decoration: const InputDecoration(
                          hintText: '氏名',
                          isDense: true,
                          border: OutlineInputBorder(),
                          contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                        ),
                        onChanged: (_) => setState(() {}),
                      ),
                    ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 8),

        // ＋/− 見出し ＋ 本体（1..8）＋ 小計 ＋ 合計
        _paperCard(
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: ConstrainedBox(
              constraints: BoxConstraints(minWidth: cornerW + cellW * players * 2),
              child: Table(
                columnWidths: widths,
                border: TableBorder.all(color: Colors.black12),
                defaultVerticalAlignment: TableCellVerticalAlignment.middle,
                children: [
                  // ＋/−ヘッダ
                  TableRow(
                    decoration: const BoxDecoration(color: Color(0xFFF0F0F0)),
                    children: [
                      const SizedBox(height: 36),
                      for (int p = 0; p < players; p++) ...[
                        _cellCenter(const Text('＋')),
                        _cellCenter(const Text('−')),
                      ],
                    ],
                  ),
                  // 本体 1..8
                  for (int r = 0; r < rounds; r++)
                    TableRow(
                      children: [
                        _cellCenter(Text('${r + 1}')),
                        for (int p = 0; p < players; p++) ...[
                          _cellEditor(_plusCtrls[p][r], onTap: () => _openInputDock(p: p, r: r, isPlus: true)),
                          _cellEditor(_minusCtrls[p][r], onTap: () => _openInputDock(p: p, r: r, isPlus: false)),
                        ],
                      ],
                    ),
                  // 小計
                  TableRow(
                    decoration: const BoxDecoration(color: Color(0xFFF7F7F7)),
                    children: [
                      _cellCenter(const Text('小 計', style: TextStyle(fontWeight: FontWeight.w600))),
                      for (int p = 0; p < players; p++) ...[
                        _cellRight(Text(_sumPlus(p).toString())),
                        _cellRight(Text(_sumMinus(p).toString())),
                      ],
                    ],
                  ),
                  // 合計（差分）
                  TableRow(
                    decoration: const BoxDecoration(color: Color(0xFFF0F0F0)),
                    children: [
                      _cellCenter(const Text('合 計', style: TextStyle(fontWeight: FontWeight.w700))),
                      for (int p = 0; p < players; p++) ...[
                        _cellRight(Text(
                          _total(p).toString(),
                          style: const TextStyle(fontWeight: FontWeight.w700),
                        )),
                        const SizedBox.shrink(), // 右側の空セル
                      ],
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }

  // ---- ボトムシート（大型入力） ----
  void _openInputDock({required int p, required int r, required bool isPlus}) {
    TextEditingController ctrl = isPlus ? _plusCtrls[p][r] : _minusCtrls[p][r];
    String text = ctrl.text.trim();

    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      useSafeArea: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (ctx) {
        return StatefulBuilder(
          builder: (ctx, setM) {
            void setText(String v) => setM(() => text = v);
            int _asInt() => int.tryParse(text.isEmpty ? '0' : text) ?? 0;

            void applyChip(int delta) {
              final v = _asInt() + delta;
              setText(v.toString());
            }

            void commit({bool moveNext = false}) {
              ctrl.text = text;
              setState(() {}); // 集計更新
              if (moveNext || _autoNext) {
                // 次の回へ（同じ列・同じ符号）
                final nextR = (r + 1) % rounds;
                r = nextR;
                ctrl = isPlus ? _plusCtrls[p][r] : _minusCtrls[p][r];
                text = ctrl.text.trim();
                setM(() {}); // 表示更新
              } else {
                Navigator.pop(ctx);
              }
            }

            return Padding(
              padding: EdgeInsets.only(
                bottom: MediaQuery.of(ctx).viewInsets.bottom,
                left: 12, right: 12, top: 10,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // タイトル
                  Row(
                    children: [
                      Text(
                        '${_nameCtrls[p].text.isEmpty ? ['東家','南家','西家','北家'][p] : _nameCtrls[p].text} / ${r + 1}回 / ${isPlus ? '＋' : '−'}',
                        style: const TextStyle(fontWeight: FontWeight.w600),
                      ),
                      const Spacer(),
                      IconButton(
                        onPressed: () => Navigator.pop(ctx),
                        icon: const Icon(Icons.close),
                      ),
                    ],
                  ),

                  // 大型入力欄
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          readOnly: true, // 自前テンキーを使う
                          controller: TextEditingController(text: text),
                          textAlign: TextAlign.right,
                          style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                          decoration: const InputDecoration(
                            border: OutlineInputBorder(),
                            contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 14),
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Column(
                        children: [
                          ElevatedButton(
                            onPressed: () => commit(moveNext: false),
                            child: const Text('セット'),
                          ),
                          const SizedBox(height: 6),
                          OutlinedButton(
                            onPressed: () => commit(moveNext: true),
                            child: const Text('セット→次'),
                          ),
                        ],
                      ),
                    ],
                  ),

                  const SizedBox(height: 10),

                  // テンキー
                  GridView.count(
                    shrinkWrap: true,
                    crossAxisCount: 3,
                    crossAxisSpacing: 8,
                    mainAxisSpacing: 8,
                    children: [
                      for (final k in ['7','8','9','4','5','6','1','2','3'])
                        _keyBtn(k, () => setText((text == '0' ? '' : text) + k)),
                      _keyBtn('±', () {
                        if (text.startsWith('-')) setText(text.substring(1));
                        else if (text.isEmpty || text == '0') setText('-');
                        else setText('-$text');
                      }),
                      _keyBtn('0', () => setText((text == '0' ? '0' : (text + '0')))),
                      _keyBtn('⌫', () {
                        if (text.isEmpty) return;
                        final v = text.substring(0, text.length - 1);
                        setText(v);
                      }),
                    ],
                  ),

                  const SizedBox(height: 10),

                  // チップ & オプション
                  Row(
                    children: [
                      Wrap(
                        spacing: 8,
                        children: [
                          for (final d in [100, 300, 500]) OutlinedButton(onPressed: () => applyChip(d), child: Text('+$d')),
                          for (final d in [-100, -300, -500]) OutlinedButton(onPressed: () => applyChip(d), child: Text('$d')),
                        ],
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Checkbox(
                        value: _autoNext,
                        onChanged: (v) => setM(() => _autoNext = v ?? false),
                      ),
                      const Text('セット後に次の回へ'),
                      const Spacer(),
                      TextButton(
                        onPressed: () {
                          setText('');
                        },
                        child: const Text('クリア'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                ],
              ),
            );
          },
        );
      },
    );
  }

  // ---- 小さなUIヘルパ ----
  Widget _paperCard({required Widget child}) => Card(
        elevation: 1,
        color: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        child: Padding(padding: const EdgeInsets.all(8.0), child: child),
      );

  Widget _cellCenter(Widget child) => Container(
        alignment: Alignment.center,
        padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 6),
        child: DefaultTextStyle.merge(style: const TextStyle(fontSize: 13), child: child),
      );

  Widget _cellRight(Widget child) => Container(
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 8),
        child: DefaultTextStyle.merge(style: const TextStyle(fontSize: 13), child: child),
      );

  Widget _cellEditor(TextEditingController ctrl, {required VoidCallback onTap}) => Padding(
        padding: const EdgeInsets.all(4.0),
        child: TextField(
          controller: ctrl,
          readOnly: true, // 直接は編集せず、ボトムシートで入力
          textAlign: TextAlign.right,
          style: const TextStyle(fontSize: 13),
          decoration: const InputDecoration(
            hintText: '0',
            isDense: true,
            contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 10),
            border: OutlineInputBorder(),
          ),
          onTap: onTap,
        ),
      );

  Widget _keyBtn(String label, VoidCallback onPressed) => ElevatedButton(
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFFF2F4F7),
          foregroundColor: Colors.black87,
          elevation: 0,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          padding: const EdgeInsets.symmetric(vertical: 12),
        ),
        child: Text(label, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
      );
}
