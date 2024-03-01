import fetch from "node-fetch";
import fs from "fs/promises";

async function getOrCreateTagId(tagName, wpUrl, wpUsername, wpPassword) {
  const tagsResponse = await fetch(
    `${wpUrl}/wp-json/wp/v2/tags?search=${tagName}`,
    {
      method: "GET",
      headers: {
        Authorization:
          "Basic " +
          Buffer.from(wpUsername + ":" + wpPassword).toString("base64")
      }
    }
  );
  const tags = await tagsResponse.json();

  if (tags.length > 0) {
    // 태그가 이미 존재하면 첫 번째 태그의 ID 반환
    return tags[0].id;
  } else {
    // 태그가 존재하지 않으면 새로 생성
    const createTagResponse = await fetch(`${wpUrl}/wp-json/wp/v2/tags`, {
      method: "POST",
      headers: {
        Authorization:
          "Basic " +
          Buffer.from(wpUsername + ":" + wpPassword).toString("base64"),
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name: tagName })
    });
    const newTag = await createTagResponse.json();
    return newTag.id;
  }
}

async function uploadPostWithTags(
  title,
  content,
  imageUrl,
  tagNames,
  wpUrl,
  wpUsername,
  wpPassword
) {
  const tagIds = await Promise.all(
    tagNames.map((tagName) =>
      getOrCreateTagId(tagName, wpUrl, wpUsername, wpPassword)
    )
  );

  // 이미지 URL을 content에 HTML img 태그로 포함
  const fullContent = `${content}<br><img src="${imageUrl}" alt="Image">`;

  // 게시물 데이터 준비
  const postData = {
    title: title,
    content: fullContent,
    status: "draft",
    tags: tagIds
  };

  // 게시물 업로드
  const postResponse = await fetch(`${wpUrl}/wp-json/wp/v2/posts`, {
    method: "POST",
    headers: {
      Authorization:
        "Basic " +
        Buffer.from(wpUsername + ":" + wpPassword).toString("base64"),
      "Content-Type": "application/json"
    },
    body: JSON.stringify(postData)
  });
  const post = await postResponse.json();
  //console.log(post);
  console.log("업로드 완료");
}

async function readDataAndUploadPost() {
  try {
    // results.json 파일에서 데이터 읽기
    const data = await fs.readFile(
      "C:/Users/yhc93/OneDrive/바탕 화면/사업문서/마/auto2/openai-env/results.json",
      "utf-8"
    );
    const jsonData = JSON.parse(data);

    // jsonData.additional_info 배열의 각 항목에 대해 반복
    for (const postInfo of jsonData.additional_info) {
      const title = postInfo[0]; // 제목
      const content = postInfo[2]; // 내용
      const imageUrl = postInfo[3].image_url; // 이미지 URL
      const tagNames = postInfo[4]; // 태그 배열

      // 게시물 업로드 함수 호출
      await uploadPostWithTags(
        title,
        content,
        imageUrl,
        tagNames,
        "https://mamania.co.kr",
        "yhc9308@naver.com",
        "Xkro owAs Pcfw 5K13 SiUi 8rby"
      );
    }
  } catch (error) {
    console.error("Error reading file or uploading post:", error);
  }
}

// 파일 읽기 및 게시물 업로드 실행
readDataAndUploadPost();
