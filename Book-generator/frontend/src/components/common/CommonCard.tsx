import bookimg from "#/assets/bookimg.jpeg";
import { Card, CardContent, CardDescription, CardTitle } from "../ui/card";

const CommonCard = () => {
  function fun1() {
    return 2 + 2;
  }
  console.log("fun1", fun1());
  const sum = () => {
    return 2 + 2;
  };
  console.log("type", typeof sum);

  return (
    <div>
      <Card className="bg-secondary-foreground w-48 h-80 rounded-sm p-3 text-black">
        <CardContent className="p-0 flex justify-center flex-col items-center">
          <img src={bookimg} alt="Logo" className="mx-auto h-64 w-full mb-2" />
          <CardTitle>title</CardTitle>
          <CardDescription className="text-black">description</CardDescription>
        </CardContent>
      </Card>
    </div>
  );
};

export default CommonCard;

