"""12주차 실습 — 성적 CSV 정제와 반별 통계 분석 (pandas만 사용)"""
import pandas as pd


def 정제(df):
    """명세서의 처리 규칙 1)~4)대로 CSV를 정제한다. 원본 df는 건드리지 않는다."""
    # 원본을 직접 고치지 않도록 복사본을 만든다
    df = df.copy()
    print("시작        ", len(df))

    # 1) 점수가 비어 있는 행을 삭제한다
    df = df.dropna(subset=["점수"])
    print("빈 칸 제거  ", len(df))

    # 2) 모든 열이 완전히 같은 행은 하나만 남긴다
    df = df.drop_duplicates()
    print("중복 제거   ", len(df))

    # 3) 반과 과목의 앞뒤 공백을 제거한다
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()

    # 4) 점수가 0~100 밖인 행을 삭제한다
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print("범위 밖 제거", len(df))

    return df


def 반별평균(df):
    """반별 개수·평균·중앙값·최댓값 표를 출력하고, 반 이름을 키로 하는 평균 Series를 반환한다."""
    # 반으로 묶어 네 가지 통계를 한 표로 만든다 (소수 둘째 자리 반올림)
    표 = df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2)
    print(표)
    # 반 이름 → 평균값
    return 표["mean"]


if __name__ == "__main__":
    # 진단 (STEP 1)
    원본 = pd.read_csv("scores_2026.csv")
    print("shape        ", 원본.shape)
    print("빈 칸 개수   ", 원본["점수"].isna().sum())
    print("중복 행 개수 ", 원본.duplicated().sum())
    print("반 종류      ", 원본["반"].unique())
    print("과목 종류    ", 원본["과목"].unique())
    print(원본["점수"].describe())

    # 인코딩이 다른 파일은 encoding="cp949"로 연다
    cp = pd.read_csv("scores_2026_cp949.csv", encoding="cp949")
    print("cp949 파일 shape", cp.shape)

    # 정제 (STEP 2)
    print("\n=== 정제 ===")
    df = 정제(원본)
    print(sorted(df["반"].unique()))
    print(sorted(df["과목"].unique()))

    # ① 필터링 (STEP 3)
    print("\n=== 필터링 ===")
    수학 = df[df["과목"] == "수학"]
    print("수학 행 수", len(수학))
    우수1반 = df[(df["반"] == "1반") & (df["점수"] >= 90)]
    print("1반 90점 이상 행 수", len(우수1반))

    # ② 그룹화
    print("\n=== 그룹화 ===")
    print(df.groupby("반")["점수"].mean())
    print(df.groupby(["과목", "반"])["점수"].mean())

    # ③ 통계
    print("\n=== 통계 ===")
    print(반별평균(df))

    # 검증 — 합계 일치와 스팟 체크
    print("\n=== 검증 ===")
    print("그룹 합계의 합", df.groupby("반")["점수"].sum().sum(), "/ 전체 합계", df["점수"].sum())
    print("그룹 개수의 합", df.groupby("반")["점수"].count().sum(), "/ 전체 행 수", len(df))
    스팟 = df[(df["반"] == "1반") & (df["과목"] == "수학")]["점수"]
    print("1반 수학 값", list(스팟), "→ 합", 스팟.sum(), "/", len(스팟), "=", 스팟.sum() / len(스팟))
