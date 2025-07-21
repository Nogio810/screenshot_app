import mss
import time
from pathlib import Path
from datetime import datetime

def capture_specific_region(x, y, width, height, filename="screenshot.png", add_timestamp=True):
    """
    指定された画面座標をキャプチャして画像ファイルとして保存します。
    
    Args:
        x (int): キャプチャ開始地点のX座標 (左上)
        y (int): キャプチャ開始地点のY座標 (左上)
        width (int): キャプチャする領域の幅
        height (int): キャプチャする領域の高さ
        filename (str): 保存する画像ファイルのパス
        add_timestamp (bool): ファイル名にタイムスタンプを追加するかどうか
    
    Returns:
        str: 保存したファイルのパス
    """
    with mss.mss() as sct:
        # キャプチャする領域を定義
        monitor = {"top": y, "left": x, "width": width, "height": height}
        
        # スクリーンショットを撮影
        sct_img = sct.grab(monitor)
        
        # タイムスタンプを追加（オプション）
        if add_timestamp:
            # ファイル名と拡張子を分離
            path = Path(filename)
            base_name = path.stem
            extension = path.suffix
            
            # 現在の日時をYYYYMMDD_HHMMSS形式で取得
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 新しいファイル名を作成
            new_filename = f"{base_name}_{timestamp}{extension}"
            output_path = path.parent / new_filename
        else:
            output_path = Path(filename)
        
        # 出力先ディレクトリが存在することを確認
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # スクリーンショットを保存
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=str(output_path))
        
        print(f"画面座標 ({x}, {y}) から幅 {width} x 高さ {height} の領域をキャプチャし '{output_path}' として保存しました。")
        return str(output_path)

def capture_with_countdown(x, y, width, height, filename="screenshot.png", countdown=3, add_timestamp=True):
    """
    カウントダウン後に指定領域をキャプチャします。
    
    Args:
        x, y, width, height: キャプチャ領域の座標と大きさ
        filename: 保存先ファイル名
        countdown: カウントダウン秒数
        add_timestamp: ファイル名にタイムスタンプを追加するかどうか
    """
    print(f"{countdown}秒後にキャプチャを開始します...")
    for i in range(countdown, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    return capture_specific_region(x, y, width, height, filename, add_timestamp)

if __name__ == "__main__":
    # 例1: 3秒のカウントダウン後に領域をキャプチャ（タイムスタンプ付き）
    capture_with_countdown(380, 230, 1400, 790, "C:/Users/takuj/Pictures/PythonScreenShot/Intellectual_Property_Rights.png", add_timestamp=True)
    
    # 同じ名前で2回目のキャプチャを行っても、タイムスタンプが異なるので上書きされません
    # time.sleep(2)  # わかりやすくするために少し待機
    # capture_with_countdown(670, 530, 1120, 635, "screenshots/region1.png", add_timestamp=True)
    
    # タイムスタンプなしで上書き保存する場合（注意：前のファイルは上書きされます）
    # capture_with_countdown(670, 530, 1120, 635, "screenshots/fixed_name.png", add_timestamp=False)