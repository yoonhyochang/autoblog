import fetch from "node-fetch";
import fs from "fs/promises";
import { writeFile, unlink } from "fs/promises"; // writeFile과 unlink를 명시적으로 임포트합니다.

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
    return tags[0].id;
  } else {
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

async function downloadImage(imageUrl) {
  const response = await fetch(imageUrl);
  if (!response.ok)
    throw new Error(`Failed to download image: ${response.statusText}`);
  const buffer = await response.buffer();
  const tempPath = `downloaded_image_${Date.now()}.jpg`; // 임시 파일 이름 생성
  await writeFile(tempPath, buffer); // 이미지를 임시 파일로 저장
  return tempPath;
}

async function uploadImage(imagePath, wpUrl, wpUsername, wpPassword) {
  const imageData = await fs.readFile(imagePath);
  const response = await fetch(`${wpUrl}/wp-json/wp/v2/media`, {
    method: "POST",
    headers: {
      Authorization:
        "Basic " +
        Buffer.from(wpUsername + ":" + wpPassword).toString("base64"),
      "Content-Disposition":
        'attachment; filename="' + imagePath.split("/").pop() + '"',
      "Content-Type": "image/jpeg"
    },
    body: imageData
  });
  const data = await response.json();
  return data.id; // 업로드된 이미지의 ID 반환
}

async function handleImageUpload(imageUrl, wpUrl, wpUsername, wpPassword) {
  try {
    const localImagePath = await downloadImage(imageUrl); // 이미지를 다운로드
    const imageId = await uploadImage(
      localImagePath,
      wpUrl,
      wpUsername,
      wpPassword
    ); // 다운로드된 이미지를 업로드하고 ID를 얻음
    await unlink(localImagePath); // 임시 파일 삭제
    return imageId; // 업로드된 이미지의 ID 반환
  } catch (error) {
    console.error("Error handling image upload:", error);
  }
}

async function uploadPostWithTags(
  title,
  content,
  imageUrl, // 원격 이미지 URL
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

  const imageId = await handleImageUpload(
    imageUrl,
    wpUrl,
    wpUsername,
    wpPassword
  ); // 원격 이미지 처리

  const postData = {
    title,
    content,
    status: "draft",
    tags: tagIds,
    featured_media: imageId
  };

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
  console.log("업로드 완료");
}

async function readDataAndUploadPost() {
  try {
    const data = await fs.readFile(
      "C:\\Users\\yhc93\\OneDrive\\바탕 화면\\사업문서\\마\\auto2\\openai-env\\result\\market_research_results.json",
      "utf-8"
    );
    const jsonData = JSON.parse(data);

    for (const postInfo of jsonData.additional_info) {
      const title = postInfo[0];
      const content = postInfo[2];
      const imageUrl = postInfo[3].image_url; // 원격 이미지 URL
      const tagNames = postInfo[4];

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

readDataAndUploadPost(); // 스크립트 실행
